# Planner Contract

## Назначение
Минимальный Planner layer переводит high-level задачу в структурированные task objects перед попаданием в queue.

## Обязательная структура task object
- `goal`
- `task_id`
- `title`
- `description`
- `plan`
- `depends_on`
- `success_criteria`
- `review_required`
- `execution_path`
- `initial_status`

## Runtime contract
Каждая задача, созданная planner runtime utility, должна содержать минимум:
- `id`
- `title`
- `status = pending`
- `plan`
- `success_criteria`
- `review_required` или `review_decision`
- `depends_on`
- `created_by = planner`
- `execution_mode = planned`

## Поддерживаемые режимы
- `single-task`
- `linear-decomposition`

## Ограничение
Это минимальный planner contract layer без advanced AI planning, без внешних интеграций и без сложного DAG engine.
