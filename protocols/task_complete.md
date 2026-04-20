---
version: 1.5.1
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/protocols/task_complete.md
implementation: mandatory
applies_to:
  - small
  - medium
  - large
---

# task_complete.md

## Purpose

This protocol defines canonical completion reporting for non-trivial work.

It is a framework input.
Project skills derived from it must be standalone project artifacts.

---

# Mandatory Implementation Rules

Any project skill derived from this protocol must:
- stay scoped to non-trivial work
- preserve the exact three-column closure table
- report actual execution, not an idealized plan
- make skipped or changed steps visible
- avoid reopening routing or redesigning the pipeline after the fact

Projects may add minimal repository-specific adaptation around wording or examples.

---

# When Task-Complete Applies

`task-complete` applies when:
- a task is non-trivial
- work ran through a routed multi-step path
- the user needs an explicit closure record

It does not apply:
- to trivial tasks
- to isolated single-step low-risk work
- to purely cosmetic changes

---

# Core Rules

## 1. Centralized Exit Gate

The routing layer is responsible for appending `task-complete` as the final step of every non-trivial pipeline.

Pipelines and execution skills should not each restate that rule.

## 2. Exact Report Format

The output must be a markdown table with exactly these columns:

| Step | Skill / Agent | Comment |
|------|---------------|---------|

Do not rename the columns.
Do not add extra columns.

## 3. Every Executed Step Must Appear

Every executed step must appear as a row in the table.

If a planned step was skipped, include it and explain why in `Comment`.

## 4. Comment Rules

Leave `Comment` blank unless:
- a step was skipped
- execution deviated from the plan
- the user should notice something incomplete or unusual

Skipped steps must always include a comment.

## 5. Closure, Not Re-Planning

`task-complete` reports what happened.
It does not invent new steps or reopen orchestration.

---

# Output Contract

At the end of a non-trivial task, produce the closure table before declaring completion.
