# Task Queue Rules

## Основной цикл
1. Orchestrator принимает задачу.
2. Задача добавляется в `task_queue.json` со статусом `pending`.
3. При начале работы задача переводится в `running`.
4. Если задача не выполнена или проверка не пройдена — статус `failed`.
5. Если задача завершена и принята — статус `done`.

## Правила переходов
- `pending -> running`
- `running -> failed`
- `running -> done`
- `failed -> running` при повторной попытке

## Правило согласования с workflow
- задача не может перейти в `done`, пока не выполнены обязательные стадии workflow
- для coding-задач это минимум: plan -> code -> test -> review

## Правило фиксации
При каждом важном переходе нужно обновлять:
- `task_queue.json`
- `task_queue_state.md`
- при значимых изменениях также `progress_log.md`
