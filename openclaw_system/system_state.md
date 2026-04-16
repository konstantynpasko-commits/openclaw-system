# System State

## Baseline
- Baseline name: `orchestration-core-v1`
- Status: `frozen`
- Scope: `minimal working orchestration core`
- Next decision required before further expansion

## Что входит в baseline v1
- `runtime/task_runner.py` как execution center
- review / fix loop
- `runtime/memory.py` и memory index/search
- `runtime/task_queue.py`
- queue hardening
- dependency orchestration
- dependency safety validation
- git layer
- GitHub remote
- GitHub Actions foundation

## Minimal planner layer
- planner contract: `openclaw_system/planner_contract.md`
- planner runtime utility: `runtime/planner.py`
- поддерживаются режимы:
  - `single-task`
  - `linear-decomposition`
- planner создаёт tasks со статусом `pending`, `created_by=planner`, `execution_mode=planned`

## Что уже работает
- normal task execution path через runner
- queue lifecycle для задач
- retry/lock/dependency checks в queue
- self/missing/cycle dependency blocking
- baseline git repo + origin/main
- foundation-check workflow зафиксирован в репозитории
- planner формализует high-level task -> structured tasks

## Что не входит в frozen baseline
- advanced planner
- parallel execution
- advanced DAG orchestration
- full CI/CD pipeline
- deployment
- observability/dashboard
- внешние интеграции как часть orchestration core

## Честная оценка
- это всё ещё минимальный orchestration core
- planner пока минимальный utility layer, не advanced planning engine
