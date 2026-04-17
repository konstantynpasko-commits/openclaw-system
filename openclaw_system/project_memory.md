# Project Memory

## Baseline v1.2
- Baseline name: `orchestration-core-v1.2`
- Status: `frozen`
- Scope: `runner + review/fix loop + memory retrieval + queue + queue hardening + dependency orchestration + dependency safety + planner contract + decomposition + verified planner handshake + command layer v1 + observability v1`
- Next decision required before further expansion

## Что входит в baseline v1.2

### Core
- `runtime/task_runner.py`
- review / fix loop
- `runtime/memory.py` + memory index/search
- `runtime/task_queue.py`
- queue hardening
- dependency orchestration
- dependency safety validation

### Planner
- `openclaw_system/planner_contract.md`
- `runtime/planner.py`
- single-task planning
- linear decomposition planning
- Planner-to-Queue Handshake VERIFIED
- verified chain:
  - `planner -> tasks.json -> queue -> runner -> review -> done`

### Observability v1
- `runtime/observability.py`
- CLI only
- reads `memory/tasks.json`
- commands:
  - `/summary`
  - `/blocked`
  - `/chain <task_id>`
- no UI
- no dashboard
- no web interface

### Command Layer v1 (Telegram control)
- `runtime/commands.py`
- Telegram is the minimal control interface over existing runtime modules
- commands:
  - `/new_goal <text>` -> planner -> `tasks.json`
  - `/run_next` -> queue -> runner -> review -> done
  - `/summary`
  - `/blocked`
  - `/chain <task_id>`
- parser is simple `startswith`
- no NLP
- no complex routing
- no new architecture

### Git / CI state
- git layer
- GitHub remote
- GitHub Actions foundation

## Что НЕ входит в baseline v1.2
- advanced planner
- parallel execution
- external integrations (`n8n`, API)
- UI layer
- advanced observability
- advanced DAG orchestration
- full CI pipeline
- complex routing

## Freeze note
- baseline v1.2 фиксирует подтверждённое состояние системы после добавления command layer v1
- это freeze состояния, без нового runtime-функционала
