#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
TASKS_PATH = WORKSPACE / 'memory' / 'tasks.json'
RUNNER_PATH = WORKSPACE / 'runtime' / 'task_runner.py'
RUNTIME_LOG = WORKSPACE / 'memory' / 'runtime-log.jsonl'
LOCK_PATH = WORKSPACE / 'runtime' / 'task_queue.lock'

PRIORITY_STATUSES = ['fix_required', 'pending']
FINAL_STATUSES = {'done', 'fix_required', 'failed'}
RUNNABLE_STATUSES = {'pending', 'fix_required'}
ALLOWED_TRANSITIONS = {
    'pending': {'running'},
    'fix_required': {'running', 'failed'},
    'running': {'done', 'fix_required', 'failed'},
    'failed': set(),
    'done': set(),
    'blocked': set(),
}
MAX_RETRY_COUNT = 2


def ts():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def load_tasks():
    print('TASKS_PATH =', TASKS_PATH)
    return json.loads(TASKS_PATH.read_text(encoding='utf-8'))


def save_tasks(tasks):
    TASKS_PATH.write_text(json.dumps(tasks, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def log_event(event, status, **extra):
    payload = {
        'ts': ts(),
        'kind': 'task_queue',
        'event': event,
        'status': status,
    }
    payload.update(extra)
    with RUNTIME_LOG.open('a', encoding='utf-8') as f:
        f.write(json.dumps(payload, ensure_ascii=False) + '\n')


def get_task(task_id, tasks=None):
    tasks = tasks or load_tasks()
    for task in tasks:
        if task.get('id') == task_id:
            return task
    return None


def validate_transition(current_status, new_status):
    allowed = ALLOWED_TRANSITIONS.get(current_status, set())
    return new_status in allowed


def set_task_status(task_id, new_status):
    tasks = load_tasks()
    task = get_task(task_id, tasks)
    if not task:
        raise RuntimeError(f'task not found: {task_id}')
    current_status = task.get('status')
    if current_status == new_status:
        return task
    if not validate_transition(current_status, new_status):
        log_event('invalid_transition', 'blocked', task_id=task_id, from_status=current_status, to_status=new_status)
        raise RuntimeError(f'invalid transition: {current_status} -> {new_status}')
    task['status'] = new_status
    task['updated_at'] = ts()[:10]
    save_tasks(tasks)
    log_event('status_transition', 'ok', task_id=task_id, from_status=current_status, to_status=new_status)
    return task


def acquire_lock():
    try:
        fd = os.open(str(LOCK_PATH), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(json.dumps({'pid': os.getpid(), 'ts': ts()}))
        log_event('lock_acquired', 'ok', lock_path=str(LOCK_PATH), pid=os.getpid())
        return True
    except FileExistsError:
        log_event('lock_acquired', 'blocked', lock_path=str(LOCK_PATH), pid=os.getpid())
        return False


def release_lock():
    if LOCK_PATH.exists():
        LOCK_PATH.unlink()
        log_event('lock_released', 'ok', lock_path=str(LOCK_PATH), pid=os.getpid())


def get_next_task():
    tasks = load_tasks()
    for wanted in PRIORITY_STATUSES:
        for task in tasks:
            if task.get('status') == wanted:
                return task
    return None


def list_tasks():
    tasks = load_tasks()
    return [
        {
            'id': task.get('id'),
            'status': task.get('status'),
            'title': task.get('title'),
        }
        for task in tasks
    ]


def _bump_retry_or_fail(task_id, current_status):
    tasks = load_tasks()
    task = get_task(task_id, tasks)
    retry_count = int(task.get('retry_count', 0)) + 1
    task['retry_count'] = retry_count
    task['updated_at'] = ts()[:10]
    if retry_count > MAX_RETRY_COUNT:
        if current_status != 'failed':
            if not validate_transition(current_status, 'failed'):
                log_event('invalid_transition', 'blocked', task_id=task_id, from_status=current_status, to_status='failed')
                raise RuntimeError(f'invalid transition: {current_status} -> failed')
            task['status'] = 'failed'
        save_tasks(tasks)
        log_event('retry_limit_exceeded', 'failed', task_id=task_id, retry_count=retry_count)
        return 'failed', retry_count
    save_tasks(tasks)
    log_event('retry_incremented', 'ok', task_id=task_id, retry_count=retry_count)
    return task.get('status'), retry_count


def run_next_task():
    if not acquire_lock():
        return {
            'ok': False,
            'message': 'queue already running',
            'lock_path': str(LOCK_PATH),
        }

    try:
        task = get_next_task()
        if not task:
            return {
                'ok': True,
                'message': 'no runnable tasks',
            }

        task_id = task['id']
        previous_status = task['status']
        if previous_status not in RUNNABLE_STATUSES:
            log_event('task_not_runnable', 'blocked', task_id=task_id, status=previous_status)
            return {
                'ok': False,
                'task_id': task_id,
                'message': f'task not runnable from status {previous_status}',
            }

        set_task_status(task_id, 'running')

        cmd = ['python3', str(RUNNER_PATH), task_id]
        result = subprocess.run(cmd, cwd=str(WORKSPACE), text=True, capture_output=True)

        tasks = load_tasks()
        updated = get_task(task_id, tasks)
        final_status = updated.get('status') if updated else 'failed'

        if final_status not in FINAL_STATUSES:
            final_status = 'failed' if result.returncode != 0 else 'done'
            set_task_status(task_id, final_status)

        retry_count = int(updated.get('retry_count', 0)) if updated else 0
        if final_status in {'fix_required', 'failed'}:
            final_status, retry_count = _bump_retry_or_fail(task_id, final_status)

        log_event('run_next_complete', 'ok' if result.returncode == 0 else 'failed', task_id=task_id, previous_status=previous_status, final_status=final_status, retry_count=retry_count, returncode=result.returncode)
        return {
            'ok': result.returncode == 0,
            'task_id': task_id,
            'previous_status': previous_status,
            'final_status': final_status,
            'retry_count': retry_count,
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'command': f'python3 {RUNNER_PATH} ' + task_id,
        }
    finally:
        release_lock()


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'list':
        print(json.dumps(list_tasks(), ensure_ascii=False, indent=2))
    elif len(sys.argv) == 2 and sys.argv[1] == 'next':
        task = get_next_task()
        print(json.dumps(task, ensure_ascii=False, indent=2))
    elif len(sys.argv) == 2 and sys.argv[1] == 'run-next':
        print(json.dumps(run_next_task(), ensure_ascii=False, indent=2))
    else:
        print('usage: task_queue.py list | task_queue.py next | task_queue.py run-next', file=sys.stderr)
        sys.exit(2)
