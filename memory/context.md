# Context

## Purpose
Minimal project memory layer for OpenClaw MVP.

## Main priority
Build and maintain project memory.

## Current focus
- Store projects
- Store ideas
- Store tasks
- Keep short shared context

## Constraints
- Minimal implementation
- No refactoring
- No security changes yet
- No new integrations

## Main interface
Telegram is the main interface.

## Update rules

### Create a project when
- the work has a clear goal
- the work will span multiple steps
- the work needs linked tasks or ideas

### Create an idea when
- it is a possible future feature or direction
- it is not approved as active work yet
- it may later become part of a project

### Create a task when
- there is a concrete action to do
- the action can be marked by status
- the action belongs to a project or a short standalone item

### Link task -> project
- use `project_id` in the task
- the `project_id` must match a project `id`
- if work belongs to an active project, always link it

### Mark status
Use only minimal statuses:
- project: `active`, `paused`, `done`
- idea: `open`, `approved`, `rejected`
- task: `todo`, `in_progress`, `done`

## Task intake workflow

Before processing each new task, read:
- `memory/projects.json`
- `memory/ideas.json`
- `memory/tasks.json`
- `memory/context.md`

Then apply this minimal flow:
1. Check whether the task clearly belongs to an existing project.
2. If yes, reuse that `project_id`.
3. If the task is a concrete action, create a new task entry with status `todo`.
4. When execution starts, change status to `in_progress`.
5. When execution ends, change status to `done` if completed.
6. If execution did not complete, keep status as `todo`.
