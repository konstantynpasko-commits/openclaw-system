# Project Memory

## Baseline v1
- Baseline name: `orchestration-core-v1`
- Status: `frozen`
- Scope: `minimal working orchestration core`
- Next decision required before further expansion

## Что входит в baseline v1
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

## Minimal planner layer
- создан `openclaw_system/planner_contract.md`
- создан `runtime/planner.py`
- planner пока минимальный и не является advanced planning layer
- planner умеет переводить high-level task в:
  - single-task
  - linear-decomposition
- planner записывает structured tasks в `memory/tasks.json`

## Что уже работает
- task-based execution идёт через `runtime/task_runner.py`
- review/fix loop работает как обязательный runtime path
- memory retrieval слой работает через `runtime/memory.py`
- queue умеет выбирать, запускать и переводить задачи по базовому lifecycle
- queue hardening закрывает повторный выбор `running`, минимальный retry и lock file
- dependency orchestration поддерживает `depends_on`
- dependency safety валидирует self/missing/cycle ошибки
- git baseline создан и запушен
- GitHub remote подключён
- foundation Actions workflow создан и запушен
- minimal planner contract layer создан и пишет planned tasks

## Что считается минимально рабочим orchestration core
- runner + review gate
- memory retrieval
- queue + queue hardening
- dependency orchestration + safety
- git/GitHub baseline
- minimal GitHub Actions foundation checks
- minimal planner contract layer

## Что НЕ входит в baseline v1
- advanced planner layer
- n8n / Telegram integration как часть orchestration baseline
- observability dashboard
- full CI pipeline
- parallel execution
- advanced DAG orchestration
- deployment / release automation
- AI planning / adaptive decomposition

## Честная оценка
- baseline v1 остаётся frozen как orchestration core
- planner layer добавлен поверх baseline минимально и без смены архитектуры
