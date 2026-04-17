# System State

## Baseline
- Baseline name: `orchestration-core-v1.2`
- Status: `frozen`
- Scope: `runner + review/fix loop + memory retrieval + queue + queue hardening + dependency orchestration + dependency safety + planner contract + decomposition + verified planner handshake + command layer v2 + observability v2 + output polish v1 + metadata normalization v1 + metadata enforcement v1`
- Next decision required before further expansion

## Frozen baseline contents

### Core
- `runtime/task_runner.py` as execution center
- review / fix loop
- `runtime/memory.py` and memory index/search
- `runtime/task_queue.py`
- queue hardening
- dependency orchestration
- dependency safety validation

### Planner
- planner contract: `openclaw_system/planner_contract.md`
- planner runtime utility: `runtime/planner.py`
- `single-task`
- `linear-decomposition`
- Planner-to-Queue Handshake VERIFIED
- verified chain: `planner -> tasks.json -> queue -> runner -> review -> done`
- planner-created tasks enforce required metadata at creation time

### Observability v2 + Output Polish v1
- file: `runtime/observability.py`
- mode: CLI / text output only
- source: `memory/tasks.json`
- task-level inspection and status filters added
- output is human-readable text
- no UI
- no dashboard
- no new service

### Command Layer v2
- file: `runtime/commands.py`
- mode: minimal text command adapter
- observability fully exposed through command layer
- routing style: direct module dispatch only
- parser: `startswith`
- Telegram acts as the control interface for planner, queue, and observability
- command-created tasks enforce required metadata at creation time
- no NLP
- no new service
- no external integration layer
- command output is human-readable

### Metadata Normalization v1 + Enforcement v1
- files:
  - `runtime/normalize_tasks.py`
  - `runtime/metadata_enforcement_probe.py`
- normalization updates old tasks by adding missing fields only
- enforcement guarantees new tasks include:
  - `created_by`
  - `execution_mode`
  - `last_test_status`
  - `last_review_status`
  - `depends_on`
- existing values are preserved

### Git / CI
- git layer
- GitHub remote
- GitHub Actions foundation

## Not in baseline v1.2
- advanced planner
- parallel execution
- external integrations (`n8n`, API)
- UI layer
- advanced observability beyond CLI task inspection and filters
- advanced DAG orchestration
- full CI pipeline
- complex routing

## Honest status
- baseline v1.2 remains minimal orchestration core
- metadata enforcement v1 changes task creation defaults only
- planner / queue / runner execution logic was not changed in this step
- further expansion requires explicit next decision
