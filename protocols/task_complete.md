---
version: 1.2.1
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/protocols/task_complete.md
---

# task_complete.md

## Purpose

This document defines the canonical protocol for `task-complete` behavior across any project built with this framework.

This is a **reference document**, not a skill.
Skills reference this document. They do not redefine it.

---

# Project Applicability

Applies to:
- small projects
- medium projects
- large projects

Implementation status:
- mandatory in every project
- invoked only for non-trivial work

---

# Protocol Template

## Mandatory

- Any task-complete skill must reference this protocol rather than restating it inline.
- The manager must enforce this protocol centrally for non-trivial pipelines.
- The skill implementing this protocol must be registered in `AGENTS.md`.

## Adapt

- Projects may add local examples or wording around the closure report.
- Projects may specialize the row comments for repository-specific caveats.
- Adaptations must preserve the exact three-column report format and non-trivial scope.

---

# When Task-Complete Applies

`task-complete` applies whenever:
- a task is non-trivial
- the manager routes work through a multi-step pipeline
- the user needs an explicit closure report for completed work

`task-complete` does NOT apply:
- to trivial tasks
- to isolated, low-risk, single-step work
- to purely cosmetic changes

---

# Core Rules

## 1. Manager-Enforced Exit Gate

The manager is responsible for appending `task-complete` as the final step of every non-trivial pipeline at routing time.

Individual pipelines do NOT declare `task-complete` themselves.
Enforcement is centralized in the manager, not distributed across pipelines.

---

## 2. Exact Report Table Format

The output must be a markdown table with exactly these three columns:

| Step | Skill / Agent | Comment |
|------|---------------|---------|
| ... | ... | ... |

Do not add extra columns.
Do not rename the columns.

---

## 3. Every Executed Step Must Appear

Every executed step in the pipeline must appear as a row in the table.

If a planned step was skipped, include it as a row and explain why in `Comment`.

---

## 4. Comment Usage Rules

Leave `Comment` blank unless:
- a step deviated from the plan
- a step was skipped
- the user should pay attention to something unusual or incomplete

A skipped step must always include a comment explaining why it was skipped.

---

## 5. Closure, Not Re-Planning

`task-complete` reports what happened.
It does not redesign the pipeline, reopen routing, or invent new steps after the fact.

If work is incomplete, the report must make that visible in the relevant row comments.

---

# Output of Task-Complete

At the end of a non-trivial task, the agent must produce the closure table before declaring the task complete.

The table must reflect actual execution, not the original plan if execution changed.

---
