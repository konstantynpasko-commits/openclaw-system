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

## Что считается минимально рабочим orchestration core
- runner + review gate
- memory retrieval
- queue + queue hardening
- dependency orchestration + safety
- git/GitHub baseline
- minimal GitHub Actions foundation checks

## Что НЕ входит в baseline v1
- advanced planner layer
- n8n / Telegram integration как часть orchestration baseline
- observability dashboard
- full CI pipeline
- parallel execution
- advanced DAG orchestration
- deployment / release automation

## Честная оценка
- baseline v1 зафиксирован как первый рабочий orchestration core
- дальнейшее расширение должно идти только после отдельного решения по следующему шагу
