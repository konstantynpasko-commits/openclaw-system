# Active Context

## Current phase
- IMPLEMENTATION: Output Polish Layer v1

## Current task
- Make command output human-readable without changing command behavior.

## What was added
- human-readable `/task <task_id>` output
- human-readable `/failed`
- human-readable `/pending`
- human-readable `/running`
- updated `runtime/command_probe_task.py`
- updated `runtime/command_probe_failed.py`

## What remains true
- no architecture changes
- no planner / queue / runner changes
- no command behavior changes
- no UI
- this is output formatting only

## Next step policy
- use command layer with human-readable text output
