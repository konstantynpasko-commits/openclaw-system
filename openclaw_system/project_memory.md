# Project Memory

## Baseline v1.1
- Baseline name: `orchestration-core-v1.1`
- Status: `extended-minimal`
- Scope: `minimal working orchestration core + verified planner handshake + minimal Telegram command layer`
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

### Telegram Command Layer v1
- `runtime/commands.py`
- Telegram is now the minimal control interface over existing runtime modules
- supported commands:
  - `/new_goal <text>` -> planner
  - `/summary` -> observability summary
  - `/blocked` -> observability blocked
  - `/chain <task_id>` -> observability chain
  - `/run_next` -> task queue run-next
- parser is simple `startswith`
- no NLP
- no complex routing
- no new architecture
- no n8n

## Что НЕ входит в baseline v1.1
- advanced planner
- external integrations beyond minimal Telegram command entrypoint
- n8n
- observability/dashboard
- parallel execution
- advanced DAG orchestration
- full CI pipeline
- complex routing

## Freeze note
- baseline v1.1 фиксирует подтверждённое состояние системы после Planner-to-Queue Handshake
- Telegram Command Layer v1 добавлен как минимальная управляющая надстройка, без изменения ядра
