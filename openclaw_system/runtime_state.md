# Runtime State

## Зафиксированное текущее состояние
- Runtime сессии: `direct`
- Модель текущей сессии: `openai-codex/gpt-5.4`
- Queue depth: `0`
- Доступ к shell есть
- exec доступен
- elevated runtime доступен в текущей сессии

## PATH на момент фиксации
`/usr/local/bin:/root/.local/bin:/root/.local/share/pnpm:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/snap/bin`

## Подтверждённо доступные команды
- `/usr/bin/git`
- `/usr/bin/node`
- `/usr/bin/npm`
- `/opt/openclaw/node_modules/.bin/acpx` (есть как бинарь/симлинк)

## Подтверждённо отсутствует в PATH
- `openclaw`
- `rg`

## Практический вывод
- shell работает
- но runtime-инструменты ещё не полностью выровнены по PATH
- для нестандартных бинарей может требоваться абсолютный путь
