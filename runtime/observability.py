#!/usr/bin/env python3
import json
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
TASKS_PATH = WORKSPACE / 'memory' / 'tasks.json'
SUMMARY_ORDER = ['pending', 'running', 'fix_required', 'done', 'failed']


def load_tasks():
    return json.loads(TASKS_PATH.read_text(encoding='utf-8'))


def get_task_map(tasks):
    return {task.get('id'): task for task in tasks if task.get('id')}


def dependencies_satisfied(task, task_map):
    depends_on = task.get('depends_on', []) or []
    missing = []
    for dep_id in depends_on:
        dep = task_map.get(dep_id)
        if not dep or dep.get('status') != 'done':
            missing.append(dep_id)
    return len(missing) == 0, missing


def _display_value(value, fallback='unknown'):
    if value is None or value == '':
        return fallback
    return str(value)


def cmd_summary(tasks):
    counts = {'total': len(tasks)}
    for status in SUMMARY_ORDER:
        counts[status] = 0
    for task in tasks:
        status = task.get('status')
        if status not in counts:
            counts[status] = 0
        counts[status] += 1
    print(f"total: {counts['total']}")
    for status in SUMMARY_ORDER:
        print(f"{status}: {counts.get(status, 0)}")


def cmd_list(tasks):
    for task in tasks:
        depends_on = task.get('depends_on', []) or []
        print(json.dumps({
            'id': task.get('id'),
            'status': task.get('status'),
            'depends_on': depends_on,
            'created_by': task.get('created_by'),
            'execution_mode': task.get('execution_mode'),
        }, ensure_ascii=False))


def cmd_task(tasks, task_id):
    task_map = get_task_map(tasks)
    task = task_map.get(task_id)
    if not task:
        print(f'task not found: {task_id}', file=sys.stderr)
        sys.exit(1)
    depends_on = task.get('depends_on', []) or []
    print(f"Task: {task.get('id')}")
    print(f"Status: {_display_value(task.get('status'))}")
    print(f"Depends on: {', '.join(depends_on) if depends_on else 'none'}")
    print(f"Created by: {_display_value(task.get('created_by'))}")
    print(f"Execution: {_display_value(task.get('execution_mode'))}")
    print(f"Test: {_display_value(task.get('last_test_status'))}")
    print(f"Review: {_display_value(task.get('last_review_status'))}")


def cmd_status_filter(tasks, wanted_status):
    matched = [task.get('id') for task in tasks if task.get('status') == wanted_status]
    print(f"{wanted_status.upper()} TASKS:")
    if not matched:
        print('- none')
        return
    for task_id in matched:
        print(f"- {task_id}")


def cmd_blocked(tasks):
    task_map = get_task_map(tasks)
    blocked = []
    for task in tasks:
        if task.get('status') != 'pending':
            continue
        ok, missing = dependencies_satisfied(task, task_map)
        if not ok:
            blocked.append({
                'id': task.get('id'),
                'status': task.get('status'),
                'depends_on': task.get('depends_on', []) or [],
                'missing_dependencies': missing,
            })
    if not blocked:
        print('no blocked pending tasks')
        return
    for item in blocked:
        print(json.dumps(item, ensure_ascii=False))


def build_dependents(tasks):
    dependents = {}
    for task in tasks:
        task_id = task.get('id')
        dependents.setdefault(task_id, [])
    for task in tasks:
        for dep_id in task.get('depends_on', []) or []:
            dependents.setdefault(dep_id, []).append(task.get('id'))
    return dependents


def walk_up(task_id, task_map):
    path = []
    current = task_id
    seen = set()
    while current and current not in seen:
        seen.add(current)
        task = task_map.get(current)
        if not task:
            break
        path.append(current)
        parents = task.get('depends_on', []) or []
        current = parents[0] if parents else None
    return list(reversed(path))


def walk_down(task_id, dependents):
    path = [task_id]
    current = task_id
    seen = {task_id}
    while True:
        children = dependents.get(current, [])
        if not children:
            break
        child = sorted(children)[0]
        if child in seen:
            break
        path.append(child)
        seen.add(child)
        current = child
    return path


def cmd_chain(tasks, task_id):
    task_map = get_task_map(tasks)
    if task_id not in task_map:
        print(f'task not found: {task_id}', file=sys.stderr)
        sys.exit(1)
    dependents = build_dependents(tasks)
    up = walk_up(task_id, task_map)
    down = walk_down(task_id, dependents)
    chain = up[:-1] + down if up else down
    print(' -> '.join(chain))


def main():
    tasks = load_tasks()
    if len(sys.argv) < 2:
        print('usage: observability.py <summary|list|task|failed|pending|running|blocked|chain> [task_id]', file=sys.stderr)
        sys.exit(2)

    command = sys.argv[1]
    if command == 'summary':
        cmd_summary(tasks)
    elif command == 'list':
        cmd_list(tasks)
    elif command == 'task':
        if len(sys.argv) < 3:
            print('usage: observability.py task <task_id>', file=sys.stderr)
            sys.exit(2)
        cmd_task(tasks, sys.argv[2])
    elif command == 'failed':
        cmd_status_filter(tasks, 'failed')
    elif command == 'pending':
        cmd_status_filter(tasks, 'pending')
    elif command == 'running':
        cmd_status_filter(tasks, 'running')
    elif command == 'blocked':
        cmd_blocked(tasks)
    elif command == 'chain':
        if len(sys.argv) < 3:
            print('usage: observability.py chain <task_id>', file=sys.stderr)
            sys.exit(2)
        cmd_chain(tasks, sys.argv[2])
    else:
        print(f'unknown command: {command}', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
