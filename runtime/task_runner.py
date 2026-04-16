#!/usr/bin/env python3
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
TASKS_PATH = WORKSPACE / 'memory' / 'tasks.json'
RUNTIME_LOG = WORKSPACE / 'memory' / 'runtime-log.jsonl'
ALLOWED_REVIEW = {'OK', 'FIX'}
BYPASS_MODES = {'manual_override', 'bypass_execution'}


def ts():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def today():
    return ts()[:10]


def load_tasks():
    return json.loads(TASKS_PATH.read_text())


def save_tasks(tasks):
    TASKS_PATH.write_text(json.dumps(tasks, ensure_ascii=False, indent=2) + '\n')


def log_event(task_id, event, status, **extra):
    payload = {
        'ts': ts(),
        'kind': 'task_runner',
        'task_id': task_id,
        'event': event,
        'status': status,
    }
    payload.update(extra)
    with RUNTIME_LOG.open('a', encoding='utf-8') as f:
        f.write(json.dumps(payload, ensure_ascii=False) + '\n')


def find_task(tasks, task_id):
    for task in tasks:
        if task.get('id') == task_id:
            return task
    return None


def run_cmd(command):
    result = subprocess.run(
        command,
        shell=True,
        cwd=str(WORKSPACE),
        text=True,
        capture_output=True,
    )
    return {
        'returncode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr,
    }


def touch_runner_metadata(task):
    task['execution_mode'] = 'runner'
    task['runner_required'] = True
    task['runner_last_run_at'] = ts()
    task['updated_at'] = today()


def set_task_state(task, status, test_status=None, review_status=None):
    touch_runner_metadata(task)
    task['status'] = status
    if test_status is not None:
        task['last_test_status'] = test_status
    if review_status is not None:
        task['last_review_status'] = review_status


def mark_bypass(task, mode, reason):
    task['execution_mode'] = mode
    task['runner_required'] = True
    task['status'] = 'todo'
    task['updated_at'] = today()
    task['bypass_reason'] = reason
    task['bypass_recorded_at'] = ts()


def main_run(task_id):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if not task:
        print(f'task not found: {task_id}', file=sys.stderr)
        sys.exit(1)

    set_task_state(task, 'in_progress', test_status='not_run', review_status='not_run')
    save_tasks(tasks)
    log_event(task_id, 'runner_start', 'ok', execution_mode='runner')

    plan = task.get('plan')
    if not plan:
        set_task_state(task, 'todo', test_status='not_run', review_status='not_run')
        save_tasks(tasks)
        log_event(task_id, 'plan_check', 'blocked', reason='missing_plan', execution_mode='runner')
        print('blocked: missing plan', file=sys.stderr)
        sys.exit(1)
    log_event(task_id, 'plan_ok', 'ok', plan=plan, execution_mode='runner')

    code_command = task.get('code_command')
    if not code_command:
        set_task_state(task, 'todo', test_status='not_run', review_status='not_run')
        save_tasks(tasks)
        log_event(task_id, 'code_stage', 'blocked', reason='missing_code_command', execution_mode='runner')
        print('blocked: missing code_command', file=sys.stderr)
        sys.exit(1)

    code_result = run_cmd(code_command)
    if code_result['returncode'] != 0:
        set_task_state(task, 'todo', test_status='not_run', review_status='not_run')
        save_tasks(tasks)
        log_event(task_id, 'code_done', 'failed', command=code_command, returncode=code_result['returncode'], stdout=code_result['stdout'], stderr=code_result['stderr'], execution_mode='runner')
        print(json.dumps({'stage': 'code', **code_result}, ensure_ascii=False, indent=2))
        sys.exit(1)
    log_event(task_id, 'code_done', 'ok', command=code_command, returncode=code_result['returncode'], stdout=code_result['stdout'], stderr=code_result['stderr'], execution_mode='runner')

    test_command = task.get('test_command')
    if not test_command:
        set_task_state(task, 'todo', test_status='missing', review_status='not_run')
        save_tasks(tasks)
        log_event(task_id, 'test', 'blocked', reason='missing_test_command', execution_mode='runner')
        print('blocked: missing test_command', file=sys.stderr)
        sys.exit(1)

    test_result = run_cmd(test_command)
    if test_result['returncode'] != 0:
        set_task_state(task, 'todo', test_status='fail', review_status='not_run')
        save_tasks(tasks)
        log_event(task_id, 'test', 'fail', command=test_command, returncode=test_result['returncode'], stdout=test_result['stdout'], stderr=test_result['stderr'], execution_mode='runner')
        print(json.dumps({'stage': 'test', **test_result}, ensure_ascii=False, indent=2))
        sys.exit(1)
    log_event(task_id, 'test', 'pass', command=test_command, returncode=test_result['returncode'], stdout=test_result['stdout'], stderr=test_result['stderr'], execution_mode='runner')

    review_decision = task.get('review_decision')
    if review_decision not in ALLOWED_REVIEW:
        set_task_state(task, 'todo', test_status='pass', review_status='missing')
        save_tasks(tasks)
        log_event(task_id, 'review', 'blocked', reason='missing_or_invalid_review_decision', review_decision=review_decision, execution_mode='runner')
        print('blocked: missing or invalid review_decision', file=sys.stderr)
        sys.exit(1)

    if review_decision == 'FIX':
        set_task_state(task, 'fix_required', test_status='pass', review_status='fix')
        save_tasks(tasks)
        log_event(task_id, 'review', 'fix', review_decision=review_decision, execution_mode='runner')
        print(json.dumps({'stage': 'review', 'decision': 'FIX'}, ensure_ascii=False, indent=2))
        sys.exit(1)

    if task.get('execution_mode') != 'runner':
        set_task_state(task, 'todo', test_status='pass', review_status='ok')
        save_tasks(tasks)
        log_event(task_id, 'done_blocked', 'blocked', reason='execution_mode_not_runner', execution_mode=task.get('execution_mode'))
        print('blocked: task not executed through runner', file=sys.stderr)
        sys.exit(1)

    set_task_state(task, 'done', test_status='pass', review_status='ok')
    save_tasks(tasks)
    log_event(task_id, 'review', 'ok', review_decision=review_decision, execution_mode='runner')
    log_event(task_id, 'runner_complete', 'ok', execution_mode='runner')
    print(json.dumps({'stage': 'review', 'decision': 'OK'}, ensure_ascii=False, indent=2))
    sys.exit(0)


def main_bypass(task_id, mode, reason):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if not task:
        print(f'task not found: {task_id}', file=sys.stderr)
        sys.exit(1)
    if mode not in BYPASS_MODES:
        print(f'invalid bypass mode: {mode}', file=sys.stderr)
        sys.exit(2)
    mark_bypass(task, mode, reason)
    save_tasks(tasks)
    log_event(task_id, 'bypass_recorded', 'ok', execution_mode=mode, reason=reason)
    print(json.dumps({'task_id': task_id, 'execution_mode': mode, 'status': task['status'], 'reason': reason}, ensure_ascii=False, indent=2))
    sys.exit(0)


def main():
    if len(sys.argv) == 2:
        main_run(sys.argv[1])
    elif len(sys.argv) >= 4 and sys.argv[1] == 'bypass':
        main_bypass(sys.argv[2], sys.argv[3], ' '.join(sys.argv[4:]).strip() or 'no reason provided')
    else:
        print('usage: task_runner.py <task_id> | task_runner.py bypass <task_id> <manual_override|bypass_execution> <reason>', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
