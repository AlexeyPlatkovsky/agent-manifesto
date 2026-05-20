---
version: 2.8.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/protocols/task_complete.md
implementation: mandatory
requires_when:
  - non-trivial routed work
---

# task_complete.md

## Purpose

This protocol defines canonical completion reporting for non-trivial routed work.

It is a framework input.
Project skills derived from it must be standalone project artifacts.

---

# Mandatory Implementation Rules

Any project skill derived from this protocol must:
- stay scoped to non-trivial routed work
- preserve the exact three-column closure table
- report actual execution, not an idealized plan
- make skipped or changed steps visible
- reference the visible output artifact for each required planned routed handoff
- refuse closure when a required planned output artifact is missing
- avoid reopening routing or redesigning the pipeline after the fact

Projects may add minimal repository-specific adaptation around wording or examples.

---

# When Task-Complete Applies

`task-complete` applies when:
- a task is non-trivial
- work ran through a routed execution path
- the framework requires an explicit closure record

It does not apply:
- to trivial tasks
- to isolated single-step low-risk work
- to trivial cosmetic changes

---

# Core Rules

## 1. Centralized Exit Gate

Assume the root contract or manager-equivalent appended `task-complete` as the final step of non-trivial routed work.

Do not self-route, reopen routing, or make pipelines and execution skills repeat that enforcement rule.

## 2. Exact Report Format

The output must be a markdown table with exactly these columns:

| Step | Skill / Agent | Comment |
|------|---------------|---------|

Do not rename the columns.
Do not add extra columns.

## 3. Every Executed Step Must Appear

Every executed step must appear as a row in the table.

If a planned step was skipped, include it and explain why in `Comment`.

Every planned routed step must appear even if it was blocked before execution.

## 4. Comment Rules

For planned routed handoffs, `Comment` must reference the step's visible output artifact label or transcript location when the tool exposes one.

Also use `Comment` when:
- a step was skipped
- execution deviated from the plan
- the user should notice something incomplete or unusual

Skipped steps must always include a comment.

If a required output artifact is missing, do not declare completion. Report closure as blocked and name the missing artifact so the manager-equivalent can return to the missing step.

## 5. Closure, Not Re-Planning

`task-complete` reports what happened.
It does not invent new steps or reopen orchestration.

---

# Output Contract

At the end of non-trivial routed work, produce the closure table before declaring completion.

The artifact must begin with the project-local capability name:

`Skill: <task-complete-capability-name> - output below`
