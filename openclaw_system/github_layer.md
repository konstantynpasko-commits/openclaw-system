# GitHub Layer

## Назначение
Этот файл фиксирует базовый git/GitHub layer системы без GitHub Actions и без внешней automation.

## Роль слоя
- хранить код и системные правила в git-репозитории
- давать нормальный след изменений для foundation baseline
- удерживать runtime, openclaw_system и memory schema под version control

## Что должно вестись через git
- `runtime/` — исполняемые runtime-скрипты
- `openclaw_system/` — системные правила, состояние и слой архитектурной фиксации
- memory schema и ключевые memory-файлы структуры проекта

## Базовые правила
- прямые изменения без git-следа считаются слабым местом системы
- foundation baseline после этапов runner/review/memory/queue должен быть зафиксирован коммитом
- пока это только git layer: без CI, без GitHub Actions, без remote-automation
- значимые изменения должны оформляться отдельными понятными коммитами

## Remote connection state
- remote: configured
- branch: `main`
- upstream: configured
- access_mode: SSH
- baseline pushed: yes
- внешний GitHub connection для baseline выполнен без GitHub Actions и без CI
