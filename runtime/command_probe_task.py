#!/usr/bin/env python3
import json
from pathlib import Path
import sys

WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE / 'runtime'))
import commands  # noqa: E402


def main():
    result = commands.handle_command('/task task_stage2_review_gate_probe')
    assert result['ok'] is True
    assert result['command'] == '/task'
    assert result['task_id'] == 'task_stage2_review_gate_probe'
    payload = json.loads(result['text'])
    assert payload['id'] == 'task_stage2_review_gate_probe'
    assert payload['status'] == 'done'
    assert payload['last_test_status'] == 'pass'
    assert payload['last_review_status'] == 'ok'
    print('probe_command_task: ok')
    print(result['text'])


if __name__ == '__main__':
    main()
