# System State

## Baseline
- Baseline name: `orchestration-core-v1.1`
- Status: `extended-minimal`
- Scope: `minimal working orchestration core + verified planner handshake + minimal Telegram command layer`
- Next decision required before further expansion

## Active baseline contents

### Core
- `runtime/task_runner.py` as execution center
- review / fix loop
- `runtime/memory.py` and memory index/search
- `runtime/task_queue.py`
- queue hardening
- dependency orchestration
- dependency safety validation

### Git / CI
- git layer
- GitHub remote
- GitHub Actions foundation

### Planner
- planner contract: `openclaw_system/planner_contract.md`
- planner runtime utility: `runtime/planner.py`
- `single-task`
- `linear-decomposition`
- Planner-to-Queue Handshake
- verified chain: `planner -> tasks.json -> queue -> runner -> review -> done`

### Observability (minimal)
- file: `runtime/observability.py`
- mode: CLI / text output only
- source: `memory/tasks.json`
- commands:
  - `summary`
  - `list`
  - `blocked`
  - `chain <task_id>`
- no UI
- no dashboard
- no new service

### Telegram Command Layer v1
- file: `runtime/commands.py`
- mode: minimal text command adapter
- entrypoint commands:
  - `/new_goal <text>`
  - `/summary`
  - `/blocked`
  - `/chain <task_id>`
  - `/run_next`
- routing style: direct module dispatch only
- parser: `startswith`
- Telegram now acts as the control interface for planner, queue, and observability
- no NLP
- no new service
- no n8n
- no complex routing

## Not in baseline v1.1
- advanced planner
- external integrations beyond command entrypoint
- n8n / workflow automation
- observability/dashboard
- parallel execution
- advanced DAG orchestration
- full CI pipeline
- complex routing

## Honest status
- baseline remains minimal orchestration core
- observability layer remains CLI only
- Telegram command layer is minimal and reuses existing modules
- further expansion requires explicit next decision
