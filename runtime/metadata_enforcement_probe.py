#!/usr/bin/env python3
import json
from pathlib import Path
import sys

WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE / 'runtime'))
import planner  # noqa: E402
import commands  # noqa: E402

TASKS_PATH = WORKSPACE / 'memory' / 'tasks.json'


def main():
    original = TASKS_PATH.read_text(encoding='utf-8')
    try:
        planner_created = planner.plan_single_task(
            goal='Planner Enforcement Probe',
            title='Planner Enforcement Probe',
            description='Probe planner metadata enforcement',
        )[0]
        assert planner_created['created_by'] == 'planner'
        assert planner_created['execution_mode'] == 'planned'
        assert planner_created['last_test_status'] == 'unknown'
        assert planner_created['last_review_status'] == 'unknown'
        assert planner_created['depends_on'] == []
        print('PLANNER')
        print(json.dumps(planner_created, ensure_ascii=False, indent=2))

        TASKS_PATH.write_text(original, encoding='utf-8')
        result = commands.handle_command('/new_goal Command Enforcement Probe')
        tasks = json.loads(TASKS_PATH.read_text(encoding='utf-8'))
        command_created = next(task for task in tasks if task.get('id') == result['task_ids'][0])
        assert command_created['created_by'] == 'command'
        assert command_created['execution_mode'] == 'planned'
        assert command_created['last_test_status'] == 'unknown'
        assert command_created['last_review_status'] == 'unknown'
        assert isinstance(command_created['depends_on'], list)
        print('COMMAND')
        print(json.dumps(command_created, ensure_ascii=False, indent=2))
    finally:
        TASKS_PATH.write_text(original, encoding='utf-8')


if __name__ == '__main__':
    main()
