#!/usr/bin/env python3
import json
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
TASKS_PATH = WORKSPACE / 'memory' / 'tasks.json'


def load_tasks():
    return json.loads(TASKS_PATH.read_text(encoding='utf-8'))


def save_tasks(tasks):
    TASKS_PATH.write_text(json.dumps(tasks, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def normalize(tasks):
    updated = 0
    for task in tasks:
        changed = False
        task_id = task.get('id', '') or ''

        if 'created_by' not in task:
            task['created_by'] = 'planner' if str(task_id).startswith('planned_') else 'system'
            changed = True
        if 'execution_mode' not in task:
            task['execution_mode'] = 'unknown'
            changed = True
        if 'last_test_status' not in task:
            task['last_test_status'] = 'unknown'
            changed = True
        if 'last_review_status' not in task:
            task['last_review_status'] = 'unknown'
            changed = True
        if 'depends_on' not in task:
            task['depends_on'] = []
            changed = True

        if changed:
            updated += 1
    return tasks, updated


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) != 1 or argv[0] != 'run':
        print('usage: normalize_tasks.py run', file=sys.stderr)
        return 2

    tasks = load_tasks()
    tasks, updated = normalize(tasks)
    save_tasks(tasks)
    print(json.dumps({'ok': True, 'updated_tasks': updated, 'total_tasks': len(tasks)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
