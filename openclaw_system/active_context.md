# Active Context

## Current phase
- IMPLEMENTATION: Metadata Normalization Layer v1

## Current task
- Normalize missing metadata fields in `memory/tasks.json` without changing existing values.

## What was added
- `runtime/normalize_tasks.py`
- CLI: `python3 runtime/normalize_tasks.py run`
- `runtime/normalize_tasks_probe.py`

## What remains true
- no architecture changes
- no planner / queue / runner changes
- no execution logic changes
- only missing metadata fields are added
- existing values are preserved

## Next step policy
- keep tasks on a minimal shared metadata standard
