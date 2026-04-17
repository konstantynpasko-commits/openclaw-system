# Project Memory

## Baseline v1.2
- Baseline name: `orchestration-core-v1.2`
- Status: `frozen`
- Scope: `runner + review/fix loop + memory retrieval + queue + queue hardening + dependency orchestration + dependency safety + planner contract + decomposition + verified planner handshake + command layer v2 + observability v2 + output polish v1 + metadata normalization v1`
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

### Observability v2
- `runtime/observability.py`
- CLI only
- reads only `memory/tasks.json`
- commands:
  - `/summary`
  - `/blocked`
  - `/chain <task_id>`
  - `/task <task_id>`
  - `/failed`
  - `/pending`
  - `/running`
- task-level inspection and status filters
- human-readable text output
- no UI
- no dashboard
- no web interface

### Command Layer v2 (Telegram control)
- `runtime/commands.py`
- Telegram is the minimal control interface over existing runtime modules
- observability is fully available through commands
- execution commands remain unchanged
- parser is simple `startswith`
- no NLP
- no complex routing
- no new architecture
- commands return human-readable text

### Metadata Normalization v1
- `runtime/normalize_tasks.py`
- command: `python3 runtime/normalize_tasks.py run`
- normalizes missing task metadata fields in `memory/tasks.json`
- adds only missing fields:
  - `created_by`
  - `execution_mode`
  - `last_test_status`
  - `last_review_status`
  - `depends_on`
- existing values are preserved
- old tasks are brought to a base metadata standard

### Git / CI state
- git layer
- GitHub remote
- GitHub Actions foundation

## Что НЕ входит в baseline v1.2
- advanced planner
- parallel execution
- external integrations (`n8n`, API)
- UI layer
- advanced observability beyond CLI task inspection and filters
- advanced DAG orchestration
- full CI pipeline
- complex routing

## Freeze note
- metadata normalization v1 added baseline metadata consistency for old tasks
- runtime behavior and architecture were not changed
