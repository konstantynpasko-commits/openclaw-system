#!/usr/bin/env python3
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

import observability
import planner
import task_queue

WORKSPACE = Path(__file__).resolve().parents[1]


class CommandError(Exception):
    pass


def _proof_prefix(goal_text: str) -> str:
    return f"telegram_command_{planner.slug(goal_text)}"


def _capture_observability(command: str, task_id: str | None = None) -> str:
    tasks = observability.load_tasks()
    buf = io.StringIO()
    with redirect_stdout(buf):
        if command == 'summary':
            observability.cmd_summary(tasks)
        elif command == 'blocked':
            observability.cmd_blocked(tasks)
        elif command == 'chain':
            if not task_id:
                raise CommandError('usage: /chain <task_id>')
            observability.cmd_chain(tasks, task_id)
        else:
            raise CommandError(f'unsupported observability command: {command}')
    return buf.getvalue().strip()


def _format_tasks(created):
    lines = [f"created: {len(created)} tasks"]
    for task in created:
        deps = task.get('depends_on', []) or []
        suffix = f" depends_on={','.join(deps)}" if deps else ''
        lines.append(f"- {task.get('id')} [{task.get('status')}] {task.get('title')}{suffix}")
    return '\n'.join(lines)


def handle_command(text: str):
    raw = (text or '').strip()
    if not raw:
        raise CommandError('empty command')

    if raw.startswith('/new_goal '):
        goal_text = raw[len('/new_goal '):].strip()
        if not goal_text:
            raise CommandError('usage: /new_goal <text>')
        steps = [
            f'Plan: {goal_text}',
            f'Build: {goal_text}',
            f'Review: {goal_text}',
        ]
        planned = planner.plan_linear(
            goal=goal_text,
            title=goal_text,
            description=f'Telegram goal: {goal_text}',
            steps=steps,
            proof_prefix=_proof_prefix(goal_text),
        )
        created = planner.append_planned_tasks(planned)
        return {
            'ok': True,
            'command': '/new_goal',
            'goal': goal_text,
            'created_count': len(created),
            'task_ids': [task.get('id') for task in created],
            'text': _format_tasks(created),
        }

    if raw == '/summary':
        text_out = _capture_observability('summary')
        return {
            'ok': True,
            'command': '/summary',
            'text': text_out,
        }

    if raw == '/blocked':
        text_out = _capture_observability('blocked')
        return {
            'ok': True,
            'command': '/blocked',
            'text': text_out,
        }

    if raw.startswith('/chain '):
        task_id = raw[len('/chain '):].strip()
        if not task_id:
            raise CommandError('usage: /chain <task_id>')
        text_out = _capture_observability('chain', task_id=task_id)
        return {
            'ok': True,
            'command': '/chain',
            'task_id': task_id,
            'text': text_out,
        }

    if raw == '/run_next':
        result = task_queue.run_next_task()
        result['command'] = '/run_next'
        if result.get('stdout') or result.get('stderr'):
            parts = []
            if result.get('stdout'):
                parts.append(result['stdout'].strip())
            if result.get('stderr'):
                parts.append(result['stderr'].strip())
            result['text'] = '\n'.join(part for part in parts if part)
        else:
            result['text'] = result.get('message', '')
        return result

    raise CommandError(f'unknown command: {raw}')


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print('usage: commands.py "/new_goal <text>" | "/summary" | "/blocked" | "/chain <task_id>" | "/run_next"', file=sys.stderr)
        return 2

    try:
        result = handle_command(' '.join(argv).strip())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except CommandError as e:
        print(str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
