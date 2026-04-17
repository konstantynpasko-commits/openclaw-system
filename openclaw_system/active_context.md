# Active Context

## Current phase
- IMPLEMENTATION: Telegram Command Layer v1

## Current task
- Add minimal Telegram command control over existing planner, queue, and observability modules.

## What was added
- `runtime/commands.py`
- commands:
  - `/new_goal <text>`
  - `/summary`
  - `/blocked`
  - `/chain <task_id>`
  - `/run_next`
- `runtime/command_probe_new_goal.py`
- `runtime/command_probe_run_next.py`

## What remains true
- no new architecture
- no n8n
- no UI
- no complex routing
- planner / queue / runner stay as the core
- command parser is minimal `startswith`

## Next step policy
- use Telegram as control interface only
- keep the layer thin over existing runtime modules
