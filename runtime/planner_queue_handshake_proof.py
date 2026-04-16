#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
TASKS_PATH = WORKSPACE / 'memory' / 'tasks.json'
PLANNER = WORKSPACE / 'runtime' / 'planner.py'
QUEUE = WORKSPACE / 'runtime' / 'task_queue.py'


def load_tasks():
    return json.loads(TASKS_PATH.read_text(encoding='utf-8'))


def get_task(task_id, tasks):
    for task in tasks:
        if task.get('id') == task_id:
            return task
    return None


def run(cmd):
    result = subprocess.run(cmd, cwd=str(WORKSPACE), text=True, capture_output=True)
    if result.returncode != 0:
        raise SystemExit(result.stderr or result.stdout or f'command failed: {cmd}')
    return result.stdout


def main():
    if len(sys.argv) < 2:
        print('usage: planner_queue_handshake_proof.py <goal> [step1|step2|step3]', file=sys.stderr)
        sys.exit(2)

    goal = sys.argv[1]
    steps = sys.argv[2] if len(sys.argv) >= 3 else 'Plan handshake|Run handshake|Finalize handshake'
    proof_prefix = 'planner_queue_handshake_proof'

    planned = json.loads(run([
        'python3', str(PLANNER), 'linear-decomposition', goal,
        'Minimal end-to-end planner to queue handshake proof',
        steps, proof_prefix,
    ]))
    task_ids = [item['id'] for item in planned]

    queue_runs = []
    for _ in task_ids:
        payload = json.loads(run(['python3', str(QUEUE), 'run-next', goal]))
        queue_runs.append({
            'task_id': payload.get('task_id'),
            'previous_status': payload.get('previous_status'),
            'final_status': payload.get('final_status'),
            'returncode': payload.get('returncode'),
        })

    tasks = load_tasks()
    final_tasks = []
    for task_id in task_ids:
        task = get_task(task_id, tasks)
        final_tasks.append({
            'id': task_id,
            'status': task.get('status'),
            'depends_on': task.get('depends_on', []),
            'last_test_status': task.get('last_test_status'),
            'last_review_status': task.get('last_review_status'),
            'runner_last_run_at': task.get('runner_last_run_at'),
        })

    all_done = all(item['status'] == 'done' for item in final_tasks)
    print(json.dumps({
        'goal': goal,
        'created_task_ids': task_ids,
        'queue_runs': queue_runs,
        'final_tasks': final_tasks,
        'all_done': all_done,
    }, ensure_ascii=False, indent=2))

    if not all_done:
        sys.exit(1)


if __name__ == '__main__':
    main()
