#!/usr/bin/env python3
import json
from pathlib import Path
import sys

WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE / 'runtime'))
import commands  # noqa: E402


def main():
    result = commands.handle_command('/failed')
    assert result['ok'] is True
    assert result['command'] == '/failed'
    lines = [line for line in result['text'].splitlines() if line.strip()]
    items = [json.loads(line) for line in lines]
    assert any(item['id'] == 'task_stage4_queue_probe_fix' for item in items), items
    assert all(item['status'] == 'failed' for item in items), items
    print('probe_command_failed: ok')
    print(result['text'])


if __name__ == '__main__':
    main()
