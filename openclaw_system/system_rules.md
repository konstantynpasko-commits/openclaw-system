# System Rules

## ЖЁСТКИЕ ПРАВИЛА

- не выполнять задачи без плана
- не пропускать этап тестирования
- не пропускать этап review
- не выполнять опасные команды без явного разрешения
- не отклоняться от плана development_plan.md без объяснения
- всегда обновлять project_memory.md после значимых изменений
- для task-based execution обязательный нормальный маршрут: `plan -> code -> test -> review` только через `/root/.openclaw/workspace/runtime/task_runner.py`
- прямые task-изменения вне `task_runner.py` считаются только `manual_override` или `bypass_execution`
- bypass не считается нормальным workflow
- нормальное завершение task в статус `done` возможно только через runner-path
- прямой shell/exec/write допустим без runner только для диагностики, read-only проверок и аварийного ручного вмешательства с явной маркировкой bypass
