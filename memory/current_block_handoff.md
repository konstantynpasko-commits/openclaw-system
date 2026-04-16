# Current Block Handoff

## Goal
Build a reliable personal AI operator on top of OpenClaw, with Telegram as the main interface, project memory, coding assistance, and controlled execution.

## Current phase
Architecture stabilization for personal daily use on subscription-based model access.
Priority: predictability, low parallelism, fewer unnecessary LLM calls, avoiding rate-limit failures.

## Main interface
Telegram direct chat.

## Current problems
- Main Telegram session overheated and reached very large context.
- One persistent block was being reused too long.
- Need block-based work with easier return through memory/transcripts instead of dragging one live context.

## Decisions already made
- OpenClaw = orchestrator, memory, diagnostics, config, small direct edits.
- Codex = primary implementation backend.
- Claude is not the default automatic fallback.
- Parallelism limited to 1.
- Telegram ACP autospawn disabled.
- Session rotation configured to idleHours=2 and maxAgeHours=8.

## What we checked
- No obvious live orphan Codex/Claude processes were consuming limits at the moment of checks.
- Biggest limit drain was the overheated main session context.

## Current active project
- proj_openclaw_mvp — OpenClaw MVP

## Current plan
1. Keep work in smaller blocks.
2. Use memory files as long-term continuity.
3. Start fresh sessions for new blocks when possible.
4. Return to old blocks via transcripts/memory instead of keeping one giant live session.

## Relevant open task
- task_diagnose_llm_call_processes — in progress

## Immediate note
User explicitly wants less discussion and fewer wasteful diagnostic turns.
