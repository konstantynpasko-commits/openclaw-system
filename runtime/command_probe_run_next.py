#!/usr/bin/env python3
import json
from pathlib import Path

import commands
import task_queue

WORKSPACE = Path(__file__).resolve().parents[1]
TASKS_PATH = WORKSPACE / 'memory' / 'tasks.json'
RUNTIME_DIR = WORKSPACE / 'runtime'


def main():
    original = TASKS_PATH.read_text(encoding='utf-8')
    goal = 'Telegram Run Next Probe Goal'
    proof_file = RUNTIME_DIR / 'telegram_command_telegram_run_next_probe_goal_1.txt'
    try:
        TASKS_PATH.write_text('[]\n', encoding='utf-8')
        created = commands.handle_command(f'/new_goal {goal}')
        result = task_queue.run_next_task(goal=goal)
        tasks = json.loads(TASKS_PATH.read_text(encoding='utf-8'))
        first_task = next(task for task in tasks if task.get('id') == created['task_ids'][0])
        assert result['ok'] is True, result
        assert result['task_id'] == created['task_ids'][0], result
        assert first_task['status'] == 'done', first_task
        assert proof_file.exists(), str(proof_file)
        assert proof_file.read_text(encoding='utf-8').strip() == f'Plan: {goal}'
        print('probe_run_next: ok')
        print(json.dumps({'task_id': result['task_id'], 'final_status': result['final_status']}, ensure_ascii=False))
    finally:
        TASKS_PATH.write_text(original, encoding='utf-8')
        if proof_file.exists():
            proof_file.unlink()


if __name__ == '__main__':
    main()
