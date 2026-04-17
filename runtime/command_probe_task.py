#!/usr/bin/env python3
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
    text = result['text']
    assert 'Task: task_stage2_review_gate_probe' in text
    assert 'Status: done' in text
    assert 'Depends on: none' in text
    assert 'Execution: runner' in text
    assert 'Test: pass' in text
    assert 'Review: ok' in text
    print('probe_command_task: ok')
    print(text)


if __name__ == '__main__':
    main()
