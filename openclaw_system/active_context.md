# Active Context

## Current phase
- IMPLEMENTATION: Observability v2

## Current task
- Extend `runtime/observability.py` for deeper task inspection and status filters.

## What was added
- `/task <task_id>`
- `/failed`
- `/pending`
- `/running`
- `runtime/observability_probe_task.py`
- `runtime/observability_probe_failed.py`

## What remains true
- no architecture changes
- no UI
- no external services
- data source is only `memory/tasks.json`
- planner / queue / runner were not changed
- this is an extension of the CLI layer only

## Next step policy
- use observability v2 for seeing tasks and problems in more detail
