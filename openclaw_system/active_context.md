# Active Context

## Текущий этап
- Planner Contract Layer

## Текущая задача
- Добавить минимальный planner contract layer поверх frozen baseline v1.

## Что уже сделано
- создан planner contract
- создан runtime planner utility
- подтверждены режимы single-task и linear-decomposition
- planner пишет structured tasks в `memory/tasks.json`

## Что остаётся правдой
- planner минимальный
- advanced planning ещё не реализован
- архитектура baseline v1 не менялась

## Следующий ожидаемый шаг
- Не добавлять advanced planner автоматически.
- Использовать текущий minimal planner contract как следующий управляемый слой над queue.
