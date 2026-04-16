# Project Memory

## Baseline v1.1
- Baseline name: `orchestration-core-v1.1`
- Status: `frozen`
- Scope: `minimal working orchestration core + verified planner handshake`
- Next decision required before further expansion

## Что входит в baseline v1.1

### Core
- `runtime/task_runner.py`
- review / fix loop
- `runtime/memory.py` + memory index/search
- `runtime/task_queue.py`
- queue hardening
- dependency orchestration
- dependency safety validation

### Git / CI
- git layer
- GitHub remote
- GitHub Actions foundation

### Planner
- `openclaw_system/planner_contract.md`
- `runtime/planner.py`
- single-task planning
- linear decomposition planning
- Planner-to-Queue Handshake
- verified end-to-end chain:
  - `planner -> tasks.json -> queue -> runner -> review -> done`

## Post-baseline layers

### Observability layer (minimal)
- `runtime/observability.py`
- CLI only
- reads `memory/tasks.json`
- commands:
  - `summary`
  - `list`
  - `blocked`
  - `chain <task_id>`
- no UI
- no dashboard
- no web interface

## Что НЕ входит в baseline v1.1
- advanced planner
- external integrations
- n8n / Telegram
- observability/dashboard
- parallel execution
- advanced DAG orchestration
- full CI pipeline

## Freeze note
- baseline v1.1 фиксирует подтверждённое состояние системы после Planner-to-Queue Handshake
- это freeze, не точка для автоматического расширения
