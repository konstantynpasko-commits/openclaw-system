# Runtime Tools Matrix

## Shell / Exec
- shell: доступен
- exec: доступен
- process control: доступен

## CLI / binaries
- git: доступен
- node: доступен
- npm: доступен
- acpx: доступен по пути `/opt/openclaw/node_modules/.bin/acpx`
- openclaw: не найден в PATH
- rg: не найден в PATH

## Operational note
Если инструмент не доступен по PATH, workflow должен:
1. либо использовать абсолютный путь
2. либо сначала зафиксировать отсутствие инструмента как runtime limitation
