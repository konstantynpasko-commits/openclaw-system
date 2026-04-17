# System State

## Baseline
- Baseline name: `orchestration-core-v1.2`
- Status: `frozen`
- Scope: `runner + review/fix loop + memory retrieval + queue + queue hardening + dependency orchestration + dependency safety + planner contract + decomposition + verified planner handshake + command layer v1 + observability v1`
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

### Observability v1
- file: `runtime/observability.py`
- mode: CLI / text output only
- source: `memory/tasks.json`
- commands:
  - `/summary`
  - `/blocked`
  - `/chain <task_id>`
- no UI
- no dashboard
- no new service

### Command Layer v1
- file: `runtime/commands.py`
- mode: minimal text command adapter
- entrypoint commands:
  - `/new_goal <text>` -> planner -> `tasks.json`
  - `/run_next` -> queue -> runner -> review -> done
  - `/summary`
  - `/blocked`
  - `/chain <task_id>`
- routing style: direct module dispatch only
- parser: `startswith`
- Telegram acts as the control interface for planner, queue, and observability
- no NLP
- no new service
- no external integration layer

### Git / CI
- git layer
- GitHub remote
- GitHub Actions foundation

## Not in baseline v1.2
- advanced planner
- parallel execution
- external integrations (`n8n`, API)
- UI layer
- advanced observability
- advanced DAG orchestration
- full CI pipeline
- complex routing

## Honest status
- baseline v1.2 is frozen
- current system is a minimal orchestration core with verified planner handshake, observability v1, and command layer v1
- further expansion requires explicit next decision
