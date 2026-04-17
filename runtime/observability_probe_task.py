#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]


def main():
    result = subprocess.run(
        ['python3', str(WORKSPACE / 'runtime' / 'observability.py'), 'task', 'task_stage2_review_gate_probe'],
        cwd=str(WORKSPACE),
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    assert payload['id'] == 'task_stage2_review_gate_probe'
    assert payload['status'] == 'done'
    assert payload['execution_mode'] == 'runner'
    assert payload['last_test_status'] == 'pass'
    assert payload['last_review_status'] == 'ok'
    print('probe_task: ok')
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == '__main__':
    main()
