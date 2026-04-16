# Repo State

## Baseline
- Baseline name: `orchestration-core-v1.1`
- Status: `frozen`
- Scope: `minimal working orchestration core + verified planner handshake`
- Next decision required before further expansion

## Frozen baseline contents
- `runtime/task_runner.py`
- review / fix loop
- `runtime/memory.py` + memory index/search
- `runtime/task_queue.py`
- queue hardening
- dependency orchestration
- dependency safety validation
- git layer
- GitHub remote
- GitHub Actions foundation
- `openclaw_system/planner_contract.md`
- `runtime/planner.py`
- single-task planning
- linear decomposition planning
- Planner-to-Queue Handshake
- verified chain: `planner -> tasks.json -> queue -> runner -> review -> done`

## Not included in baseline v1.1
- advanced planner
- external integrations
- n8n / Telegram
- observability/dashboard
- parallel execution
- advanced DAG orchestration
- full CI pipeline

## Git state
- git repository: present
- branch: `main`
- remote: `origin`
- upstream: configured
- access mode: SSH
- baseline freeze target: `orchestration-core-v1.1`
- freeze commit: cae7f8a
- push target: `origin/main`

## Freeze note
- this baseline freeze is documentation and repository state fixation only
- no new feature work is part of this step
