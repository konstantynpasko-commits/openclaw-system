# System State

## Текущий режим
- OpenClaw работает как orchestrator.
- Telegram остаётся главным интерфейсом.
- Для task-based execution нормальный обязательный маршрут зафиксирован через `/root/.openclaw/workspace/runtime/task_runner.py`.
- Поверх runner действует минимальный queue layer в `/root/.openclaw/workspace/runtime/task_queue.py`.

## Execution center baseline
- Mandatory normal path: `plan -> code -> test -> review` через `task_runner.py`
- Queue отвечает только за выбор задачи, перевод в `running`, retry_count и базовый lifecycle control
- Direct task changes вне runner считаются bypass

## Queue hardening status
- Queue hardening выполнен частично, но runtime-проверками подтверждён
- Закрыто:
  - повторный выбор задач со статусом `running`
  - минимальная защита от параллельного `run-next` через lock file
  - минимальный `retry_count` и перевод в `failed` после лимита
  - валидация допустимых lifecycle transitions
- Осталось:
  - нет полноценного file locking уровня ОС между всеми типами правок кроме lock file для queue-run
  - прямой edit/write в `memory/tasks.json` всё ещё технически возможен

## Честная оценка
- Runner остаётся отдельным исполнителем
- Queue стал жёстче и безопаснее как минимальный orchestration layer
- Но queue всё ещё опирается на файл задач и не является полностью защищённой многопроцессной системой
