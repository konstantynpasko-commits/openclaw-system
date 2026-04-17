#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]


def main():
    result = subprocess.run(
        ['python3', str(WORKSPACE / 'runtime' / 'observability.py'), 'failed'],
        cwd=str(WORKSPACE),
        text=True,
        capture_output=True,
        check=True,
    )
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    items = [json.loads(line) for line in lines]
    assert any(item['id'] == 'task_stage4_queue_probe_fix' for item in items), items
    assert all(item['status'] == 'failed' for item in items), items
    print('probe_failed: ok')
    print(json.dumps(items[:2], ensure_ascii=False))


if __name__ == '__main__':
    main()
