# System State

## Baseline
- Baseline name: `orchestration-core-v1.1`
- Status: `frozen`
- Scope: `minimal working orchestration core + verified planner handshake`
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

## Additional runtime layer

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

## Not in baseline v1.1
- advanced planner
- external integrations
- n8n / Telegram
- observability/dashboard
- parallel execution
- advanced DAG orchestration
- full CI pipeline

## Honest status
- baseline v1.1 is frozen
- current system remains minimal orchestration core
- observability layer is minimal CLI only
- further expansion requires explicit next decision
