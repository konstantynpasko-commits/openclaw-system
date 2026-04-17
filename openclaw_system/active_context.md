# Active Context

## Current phase
- IMPLEMENTATION: Metadata Enforcement Layer v1

## Current task
- Enforce full metadata on new task creation in planner and command layer.

## What was added
- planner-side metadata enforcement
- command-side metadata enforcement for `/new_goal`
- `runtime/metadata_enforcement_probe.py`

## What remains true
- no architecture changes
- no runner / queue execution changes
- no existing task breakage
- existing values are preserved
- only creation-time defaults are enforced

## Next step policy
- all new tasks should start with complete metadata
