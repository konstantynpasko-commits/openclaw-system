#!/usr/bin/env python3
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
TASKS_PATH = WORKSPACE / 'memory' / 'tasks.json'
PROJECT_ID = 'proj_openclaw_mvp'


def today():
    return datetime.now(timezone.utc).date().isoformat()


def slug(text: str) -> str:
    value = re.sub(r'[^a-zA-Z0-9]+', '_', text.strip().lower()).strip('_')
    return value or 'planned_task'


def load_tasks():
    return json.loads(TASKS_PATH.read_text(encoding='utf-8'))


def save_tasks(tasks):
    TASKS_PATH.write_text(json.dumps(tasks, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def ensure_unique_id(task_id: str, tasks):
    existing = {t.get('id') for t in tasks}
    if task_id not in existing:
        return task_id
    n = 2
    while f'{task_id}_{n}' in existing:
        n += 1
    return f'{task_id}_{n}'


def make_task(goal, task_id, title, description, plan, depends_on, success_criteria, proof_artifact=None, review_decision='OK'):
    task = {
        'goal': goal,
        'task_id': task_id,
        'id': task_id,
        'title': title,
        'description': description,
        'status': 'pending',
        'plan': plan,
        'success_criteria': success_criteria,
        'review_required': True,
        'depends_on': depends_on,
        'created_by': 'planner',
        'execution_mode': 'planned',
        'execution_path': 'task_runner',
        'initial_status': 'pending',
        'project_id': PROJECT_ID,
        'created_at': today(),
        'updated_at': today(),
    }
    if proof_artifact:
        artifact_path = f'/root/.openclaw/workspace/runtime/{proof_artifact}'
        task['code_command'] = (
            "python3 - <<'PY'\n"
            f"from pathlib import Path\nPath('{artifact_path}').write_text({title!r} + '\\n', encoding='utf-8')\n"
            "print('proof written')\nPY"
        )
        task['test_command'] = (
            "python3 - <<'PY'\n"
            "from pathlib import Path\n"
            f"p = Path('{artifact_path}')\n"
            "assert p.exists(), 'result file missing'\n"
            f"text = p.read_text(encoding='utf-8').strip()\nassert text == {title!r}, f'unexpected content: {{text!r}}'\n"
            "print('test passed')\nPY"
        )
        task['review_decision'] = review_decision
    return task


def plan_single_task(goal: str, title: str, description: str):
    base_id = slug(title)
    task_id = f'planned_{base_id}'
    return [
        make_task(
            goal=goal,
            task_id=task_id,
            title=title,
            description=description,
            plan=f'Execute task: {title}',
            depends_on=[],
            success_criteria=f'Task completed: {title}',
        )
    ]


def plan_linear(goal: str, title: str, description: str, steps, proof_prefix=None):
    tasks = []
    previous = None
    for idx, step in enumerate(steps, 1):
        task_id = f'planned_{slug(title)}_{idx}'
        proof_artifact = f'{proof_prefix}_{idx}.txt' if proof_prefix else None
        tasks.append(
            make_task(
                goal=goal,
                task_id=task_id,
                title=step,
                description=description,
                plan=f'Execute linear step {idx}: {step}',
                depends_on=[previous] if previous else [],
                success_criteria=f'Step {idx} completed: {step}',
                proof_artifact=proof_artifact,
            )
        )
        previous = task_id
    return tasks


def append_planned_tasks(new_tasks):
    tasks = load_tasks()
    for item in new_tasks:
        item['id'] = ensure_unique_id(item['id'], tasks)
        item['task_id'] = item['id']
        if item['depends_on']:
            updated = []
            for dep in item['depends_on']:
                updated.append(dep)
            item['depends_on'] = updated
        tasks.append(item)
    save_tasks(tasks)
    return new_tasks


def main():
    if len(sys.argv) < 4:
        print('usage: planner.py <single-task|linear-decomposition> <title> <description> [step1|step2|step3] [proof_prefix]', file=sys.stderr)
        sys.exit(2)

    mode = sys.argv[1]
    title = sys.argv[2]
    description = sys.argv[3]
    goal = title

    if mode == 'single-task':
        planned = plan_single_task(goal, title, description)
    elif mode == 'linear-decomposition':
        raw_steps = sys.argv[4] if len(sys.argv) >= 5 else 'Step 1|Step 2|Step 3'
        proof_prefix = sys.argv[5] if len(sys.argv) >= 6 else None
        steps = [s.strip() for s in raw_steps.split('|') if s.strip()]
        planned = plan_linear(goal, title, description, steps[:3], proof_prefix=proof_prefix)
    else:
        print(f'unknown mode: {mode}', file=sys.stderr)
        sys.exit(2)

    created = append_planned_tasks(planned)
    print(json.dumps(created, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
