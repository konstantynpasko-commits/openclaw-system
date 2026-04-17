#!/usr/bin/env python3
from pathlib import Path
import sys

WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE / 'runtime'))
import commands  # noqa: E402


def main():
    result = commands.handle_command('/failed')
    assert result['ok'] is True
    assert result['command'] == '/failed'
    text = result['text']
    assert text.startswith('FAILED TASKS:')
    assert '- task_stage4_queue_probe_fix' in text
    assert '- task_queue_harden_retry_probe' in text
    print('probe_command_failed: ok')
    print(text)


if __name__ == '__main__':
    main()
