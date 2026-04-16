# Integrations Rules

## Общие правила
1. Интеграции не должны размывать основную архитектуру ролей.
2. Внешняя интеграция должна иметь зафиксированный runtime-статус: active / partial / planned.
3. Если интеграция не подтверждена в runtime, нельзя описывать её как рабочую.
4. Интеграции должны усиливать OpenClaw, а не подменять его orchestration-логику.

## Правило для n8n
- до подтверждённой установки n8n считается planned integration layer
- после подтверждённой установки и проверки может быть переведён в active integration layer

## Правило фиксации
При изменении слоя интеграций нужно обновлять:
- integrations_state.md
- integrations_catalog.md
- project_memory.md
