---
version: 2.8.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/conventions/tool-adapters.md
---

# tool-adapters.md

## Purpose

This convention defines standards for tool-specific entry files in generated or reviewed instruction systems.

## Root Models

For single-tool projects:
- the selected tool's official native entrypoint may hold the full operational contract
- the native entrypoint must be verified against current official documentation during composition or review
- supporting artifacts should use the selected tool's native structure by default
- `AGENTS.md` is not required

For multi-tool or AI-agnostic projects:
- `AGENTS.md` is the canonical root operational contract
- every tool-specific entry file must be a thin adapter
- no tool-specific file may become a second source of truth

## Thin Adapter Requirements

A thin adapter is not a vague pointer. It must:
- state that the file is only an adapter for the named tool
- instruct the tool to read the exact canonical root contract path before starting project work
- instruct the tool to follow every applicable root contract rule
- state that the root contract overrides the adapter on conflict
- stop the tool if the root contract is unavailable

Use imperative mandatory language. Avoid adapter wording such as "see", "refer to", or "follow if needed" when the adapter is meant to impose a mandatory root contract.

