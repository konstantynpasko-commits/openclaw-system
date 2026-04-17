#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
TASKS_PATH = WORKSPACE / 'memory' / 'tasks.json'
PROBE_ID = 'probe_missing_fields_task'


def main():
    original = TASKS_PATH.read_text(encoding='utf-8')
    try:
        tasks = json.loads(original)
        probe_task = {
            'id': PROBE_ID,
            'title': 'Probe missing fields task',
            'status': 'todo',
            'project_id': 'proj_openclaw_mvp',
            'created_at': '2026-04-17',
            'updated_at': '2026-04-17'
        }
        tasks.append(probe_task)
        TASKS_PATH.write_text(json.dumps(tasks, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        before_tasks = json.loads(TASKS_PATH.read_text(encoding='utf-8'))
        before = next(task for task in before_tasks if task.get('id') == PROBE_ID)
        assert 'created_by' not in before
        assert 'execution_mode' not in before
        print('BEFORE')
        print(json.dumps(before, ensure_ascii=False, indent=2))

        subprocess.run(['python3', str(WORKSPACE / 'runtime' / 'normalize_tasks.py'), 'run'], cwd=str(WORKSPACE), check=True, text=True, capture_output=True)

        after_tasks = json.loads(TASKS_PATH.read_text(encoding='utf-8'))
        after = next(task for task in after_tasks if task.get('id') == PROBE_ID)
        assert after['created_by'] == 'system'
        assert after['execution_mode'] == 'unknown'
        assert after['last_test_status'] == 'unknown'
        assert after['last_review_status'] == 'unknown'
        assert after['depends_on'] == []
        print('AFTER')
        print(json.dumps(after, ensure_ascii=False, indent=2))
    finally:
        TASKS_PATH.write_text(original, encoding='utf-8')


if __name__ == '__main__':
    main()
