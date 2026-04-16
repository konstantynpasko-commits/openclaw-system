# GitHub Actions Layer

## Назначение
Этот файл фиксирует GitHub Actions как automation-слой для dev-проверок.

## Роль GitHub Actions
- запуск проверок при изменениях
- запуск стандартизированных workflow
- помощь в дисциплине delivery-процесса

## Базовые сценарии для GitHub Actions
- проверка структуры проекта
- запуск тестов
- запуск линтеров
- базовые smoke-проверки

## Foundation workflow
- создан workflow: `.github/workflows/foundation-check.yml`
- triggers:
  - `push` в `main`
  - `pull_request` в `main`
- что проверяется:
  - `python -m py_compile` для `runtime/task_runner.py`, `runtime/task_queue.py`, `runtime/memory.py`
  - read-only smoke checks: `python runtime/task_queue.py list` и `python runtime/memory.py search workflow`
- что пока не проверяется:
  - deployment
  - интеграции
  - GitHub Actions release flow
  - destructive task execution

## Правило
- GitHub Actions должен усиливать Tester и Reviewer, а не подменять их
- локальная проверка всё равно остаётся обязательной частью workflow системы
