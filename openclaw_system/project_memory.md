# Project Memory

## Baseline v1.2
- Baseline name: `orchestration-core-v1.2`
- Status: `frozen`
- Scope: `runner + review/fix loop + memory retrieval + queue + queue hardening + dependency orchestration + dependency safety + planner contract + decomposition + verified planner handshake + command layer v2 + observability v2 + output polish v1 + metadata normalization v1 + metadata enforcement v1`
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
- new planner-created tasks now enforce metadata:
  - `created_by=planner`
  - `execution_mode=planned`
  - `last_test_status=unknown`
  - `last_review_status=unknown`
  - `depends_on=[]` when absent

### Observability v2
- `runtime/observability.py`
- CLI only
- reads only `memory/tasks.json`
- human-readable text output

### Command Layer v2 (Telegram control)
- `runtime/commands.py`
- observability is fully available through commands
- execution commands remain unchanged
- commands return human-readable text
- new command-created tasks now enforce metadata:
  - `created_by=command`
  - `execution_mode=planned`
  - `last_test_status=unknown`
  - `last_review_status=unknown`
  - `depends_on=[]` when absent

### Metadata Normalization + Enforcement
- `runtime/normalize_tasks.py`
- `runtime/metadata_enforcement_probe.py`
- old tasks normalized to base standard
- new tasks created with full metadata by default
- existing values are preserved and not overwritten

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
- metadata enforcement v1 guarantees clean metadata for new tasks at creation time
- runtime behavior and architecture were not changed
