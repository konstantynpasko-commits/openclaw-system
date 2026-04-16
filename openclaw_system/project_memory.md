# Project Memory

## Текущий статус системы
- OpenClaw используется как основная оркестрация системы.
- Telegram является главным интерфейсом.
- Файловая память уже используется через MEMORY.md и memory/*.json/*.md.
- Task-based execution идёт через `runtime/task_runner.py`.
- Queue layer поверх runner реализован в `runtime/task_queue.py`.

## Queue hardening summary
- Проведён аудит слабых мест queue.
- Найдено до hardening:
  - нет защиты от параллельного `run-next`
  - нет retry counter
  - нет проверки lifecycle transitions
  - queue опирается на голый file state
- Усилено:
  - `running` задача не выбирается повторно как next task
  - добавлен lock file `/root/.openclaw/workspace/runtime/task_queue.lock`
  - добавлен `retry_count`
  - после превышения лимита retry задача уходит в `failed`
  - добавлена проверка допустимых переходов статусов

## Что проверено в runtime
- `task_queue.py next` не выбрал probe со статусом `running`, а выбрал `pending`
- lock file реально блокирует второй `run-next`
- `retry_count` реально увеличивается: 1 -> 2 -> 3
- после лимита retry задача реально переходит в `failed`

## Что ещё осталось слабым местом
- queue всё ещё использует файловое состояние без полного межпроцессного transactional контроля
- прямой manual edit/write в `memory/tasks.json` остаётся возможным обходом
- это минимальный hardened queue, а не полнофункциональный scheduler

## Честная оценка
- Queue hardening выполнен и подтверждён по runtime-фактам.
- Но слой остаётся минимальным и file-based.
