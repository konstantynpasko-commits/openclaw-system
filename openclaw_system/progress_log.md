# Progress Log

## 2026-04-17 — Metadata Enforcement Layer v1
- Updated `runtime/planner.py`.
- Updated `runtime/commands.py` for planner-backed command task creation.
- Added metadata enforcement for new tasks at creation time.
- Enforced fields:
  - `created_by`
  - `execution_mode`
  - `last_test_status`
  - `last_review_status`
  - `depends_on`
- Default values:
  - planner-created -> `created_by=planner`
  - command-created -> `created_by=command`
  - `execution_mode=planned`
  - `last_test_status=unknown`
  - `last_review_status=unknown`
  - `depends_on=[]` when absent
- Existing values are preserved and not overwritten.
- Added probe:
  - `runtime/metadata_enforcement_probe.py`
- New tasks now always start with full metadata.
- Planner / queue / runner execution logic was not changed.
- Honest status: RUNTIME VERIFIED.

## 2026-04-17 — Metadata Normalization Layer v1
- Created `runtime/normalize_tasks.py`.
- Added CLI command:
  - `python3 runtime/normalize_tasks.py run`
- Added normalization rules for missing fields in `memory/tasks.json`:
  - `created_by`
  - `execution_mode`
  - `last_test_status`
  - `last_review_status`
  - `depends_on`
- Rule for `created_by`:
  - `planned_*` -> `planner`
  - all others -> `system`
- Existing values are preserved.
- Missing fields only are added.
- Old tasks were normalized to a base metadata standard.
- Added probe:
  - `runtime/normalize_tasks_probe.py`
- Honest status: RUNTIME VERIFIED.

## 2026-04-17 — Output Polish Layer v1
- Updated `runtime/observability.py` output formatting.
- Human-readable text added for:
  - `/task <task_id>`
  - `/failed`
  - `/pending`
  - `/running`
- `/task` now prints labeled lines instead of JSON-in-text.
- status filter commands now print simple bullet lists.
- Updated probes:
  - `runtime/command_probe_task.py`
  - `runtime/command_probe_failed.py`
- Commands now return human-readable text.
- Planner, queue, and runner were not changed.
- Command behavior was not changed.
- Honest status: RUNTIME VERIFIED.

## 2026-04-17 — Command Layer v2
- Extended `runtime/commands.py`.
- Added command support for observability v2:
  - `/task <task_id>`
  - `/failed`
  - `/pending`
  - `/running`
- Commands reuse `runtime/observability.py`.
- Output is returned as readable text through the command layer.
- Added probes:
  - `runtime/command_probe_task.py`
  - `runtime/command_probe_failed.py`
- Observability is now fully available through Telegram commands.
- Planner, queue, and runner were not changed.
- No architecture changes.
- Honest status: RUNTIME VERIFIED.

## 2026-04-17 — Observability v2
- Extended `runtime/observability.py`.
- Added CLI commands over `memory/tasks.json`:
  - `/task <task_id>`
  - `/failed`
  - `/pending`
  - `/running`
- `/task <task_id>` reports:
  - `id`
  - `status`
  - `depends_on`
  - `created_by`
  - `execution_mode`
  - `last_test_status`
  - `last_review_status`
- Added status filters for failed, pending, and running tasks.
- Added probes:
  - `runtime/observability_probe_task.py`
  - `runtime/observability_probe_failed.py`
- Observability v2 is an extension of the CLI layer only.
- Planner, queue, and runner were not changed.
- No UI added.
- No external services added.
- Honest status: RUNTIME VERIFIED.
