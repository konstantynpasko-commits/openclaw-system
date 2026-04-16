# System Architecture

Система построена по принципу разделения ролей:

- GPT-5.4 → Planner (мозг, планирование, принятие решений)
- OpenClaw → Orchestrator (управление процессом, маршрутизация задач)
- Codex → Coder (реализация кода)
- Reviewer → отдельная модель (проверка качества)
- Tester → shell/runtime (запуск и тестирование)
- Executor → выполнение команд
- n8n → слой интеграций
- GitHub + GitHub Actions → dev-инфраструктура
- Project Memory → файловая/БД память системы
