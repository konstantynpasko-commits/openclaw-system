#!/usr/bin/env python3
import json
from pathlib import Path

import commands

WORKSPACE = Path(__file__).resolve().parents[1]
TASKS_PATH = WORKSPACE / 'memory' / 'tasks.json'


def main():
    original = TASKS_PATH.read_text(encoding='utf-8')
    goal = 'Telegram Command Probe Goal'
    try:
        result = commands.handle_command(f'/new_goal {goal}')
        tasks = json.loads(TASKS_PATH.read_text(encoding='utf-8'))
        created = [task for task in tasks if task.get('goal') == goal]
        assert result['ok'] is True
        assert result['created_count'] == 3, result
        assert len(created) == 3, created
        assert created[0]['title'] == f'Plan: {goal}'
        assert created[1]['depends_on'] == [created[0]['id']]
        assert created[2]['depends_on'] == [created[1]['id']]
        print('probe_new_goal: ok')
        print(json.dumps({'task_ids': result['task_ids']}, ensure_ascii=False))
    finally:
        TASKS_PATH.write_text(original, encoding='utf-8')


if __name__ == '__main__':
    main()
