# Memory Index

## Назначение
Точка входа в structured project memory слоя системы.

## Файлы
- `project_memory.md` — общий обзор проекта и статуса по этапам
- `project_memory_schema.md` — схема memory-слоя и правила обновления
- `system_state.md` — текущее рабочее состояние системы
- `progress_log.md` — журнал внедрённых этапов и заметных изменений
- `active_context.md` — активный рабочий контекст и ближайший следующий шаг
- `decisions_log.md` — ключевые решения по архитектуре и режиму работы
- `task_queue_schema.md` — схема task queue слоя
- `task_queue_rules.md` — правила переходов статусов задач
- `task_queue.json` — текущая очередь задач
- `task_queue_state.md` — текущее состояние очереди
- `github_layer.md` — роль GitHub в системе
- `github_actions_layer.md` — роль GitHub Actions в системе
- `github_workflow_rules.md` — правила GitHub workflow
- `github_actions_templates.md` — шаблоны сценариев для GitHub Actions
- `runtime_state.md` — фактическое состояние runtime и PATH
- `runtime_stabilization_plan.md` — план стабилизации runtime
- `runtime_tools_matrix.md` — матрица доступности runtime-инструментов
- `runtime_exec_rules.md` — правила выполнения команд в runtime
- `runtime_smoke_checklist.md` — smoke-проверка runtime
- `integrations_state.md` — фактический baseline интеграций
- `n8n_layer.md` — роль n8n в архитектуре
- `integrations_catalog.md` — каталог интеграционных направлений
- `integrations_rules.md` — правила слоя интеграций
- `n8n_activation_checklist.md` — checklist активации n8n
- `guardrails_layer.md` — guardrails как системный слой
- `risk_tiers.md` — уровни риска действий
- `approval_rules.md` — правила подтверждения действий
- `blocked_actions.md` — список запрещённых действий
- `action_limits.md` — ограничения действий системы
- `guardrails_checklist.md` — checklist перед выполнением рискованных действий
- `aux_models_layer.md` — слой вспомогательных моделей
- `aux_models_catalog.md` — каталог разрешённых вспомогательных агентов
- `model_routing_rules.md` — правила маршрутизации по моделям
- `aux_models_usage_policy.md` — политика использования вспомогательных моделей
- `model_activation_checklist.md` — checklist активации вспомогательной модели
- `bugfix_template.md` — шаблон bugfix-сценария
- `feature_template.md` — шаблон feature-сценария
- `refactor_template.md` — шаблон refactor-сценария
- `scenario_selection_rules.md` — правила выбора сценария
- `scenario_workflow_map.md` — связь сценариев с основным workflow

## Правило
Если нужно понять текущее состояние системы, начинать с:
1. `project_memory.md`
2. `system_state.md`
3. `active_context.md`
