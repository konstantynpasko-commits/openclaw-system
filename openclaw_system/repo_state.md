# Repo State

## Baseline
- Baseline name: `orchestration-core-v1.2`
- Status: `frozen`
- Scope: `runner + review/fix loop + memory retrieval + queue + queue hardening + dependency orchestration + dependency safety + planner contract + decomposition + verified planner handshake + command layer v1 + observability v1`
- Next decision required before further expansion

## Frozen baseline contents
- `runtime/task_runner.py`
- review / fix loop
- `runtime/memory.py` + memory index/search
- `runtime/task_queue.py`
- queue hardening
- dependency orchestration
- dependency safety validation
- `openclaw_system/planner_contract.md`
- `runtime/planner.py`
- Planner-to-Queue Handshake VERIFIED
- `runtime/observability.py`
- `runtime/commands.py`
- `/new_goal <text>` -> planner -> `tasks.json`
- `/run_next` -> queue -> runner -> review -> done
- `/summary`
- `/blocked`
- `/chain <task_id>`
- git layer
- GitHub remote
- GitHub Actions foundation

## Not included in baseline v1.2
- advanced planner
- parallel execution
- external integrations (`n8n`, API)
- UI layer
- advanced observability
- advanced DAG orchestration
- full CI pipeline
- complex routing

## Git state
- git repository: present
- branch: `main`
- remote: `origin`
- upstream: configured
- access mode: SSH
- baseline freeze target: `orchestration-core-v1.2`
- push target: `origin/main`

## Freeze note
- this baseline freeze is documentation and repository state fixation only
- no new feature work is part of this step
- runtime was not changed in this freeze step
