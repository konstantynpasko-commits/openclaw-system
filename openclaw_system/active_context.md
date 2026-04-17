# Active Context

## Current phase
- IMPLEMENTATION: Command Layer v2

## Current task
- Extend `runtime/commands.py` so observability v2 is fully available through Telegram commands.

## What was added
- `/task <task_id>`
- `/failed`
- `/pending`
- `/running`
- `runtime/command_probe_task.py`
- `runtime/command_probe_failed.py`

## What remains true
- no architecture changes
- no new layers
- planner / queue / runner were not changed
- parser stays minimal `startswith`
- this is only a command layer extension

## Next step policy
- use command layer v2 for full system control through Telegram
