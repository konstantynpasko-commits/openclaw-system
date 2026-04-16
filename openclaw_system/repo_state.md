# Repo State

## Baseline
- Baseline name: `orchestration-core-v1`
- Status: `frozen`
- Scope: `minimal working orchestration core`
- Next decision required before further expansion

## Что входит в baseline v1
- runner
- review loop
- memory retrieval
- queue
- queue hardening
- dependency orchestration
- dependency safety validation
- git layer
- GitHub remote
- GitHub Actions foundation

## Что НЕ входит в baseline v1
- advanced planner layer
- n8n / Telegram orchestration layer
- observability/dashboard
- full CI pipeline
- parallel execution
- advanced DAG orchestration

## Git state
- git-репозиторий: есть
- branch: `main`
- remote: configured (`origin`)
- upstream: configured
- access_mode: SSH
- baseline pushed: yes
- freeze commit: pending commit/push

## Честная оценка слоя
- baseline v1 зафиксирован локально как frozen state
- после freeze commit он должен стать основной точкой отсчёта для дальнейших решений
