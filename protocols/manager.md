---
version: 1.2.1
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/protocols/manager.md
---

# manager.md

## Purpose

This document defines the canonical protocol for `manager` behavior across projects that need centralized non-trivial routing.

This is a **reference document**, not a skill.
Skills reference this document. They do not redefine it.

---

# Project Applicability

Applies to:
- medium projects
- large projects

Implementation status:
- mandatory for medium projects
- mandatory for large projects
- avoided by default in small projects

---

# Protocol Template

## Mandatory

- Any manager skill must reference this protocol rather than restating it inline.
- The manager must stay purely responsible for routing and orchestration.
- The manager skill must be registered in `AGENTS.md`.

## Adapt

- Projects may add repository-specific workflow names and routing criteria.
- Projects may bind the manager to local validation, review, or agent capabilities.
- Adaptations must not turn the manager into an implementation skill.

---

# When Manager Applies

`manager` applies whenever:
- the project is medium or large
- a task is non-trivial
- routing must choose between multiple skills, workflows, or agents
- completion enforcement must be centralized

`manager` does NOT apply:
- to trivial tasks
- to small projects that still fit minimal inline routing
- when the user is only asking a factual question with no execution path

---

# Core Rules

## 1. Manager Is Routing Only

The manager selects and sequences capabilities.
It does not execute implementation steps itself.

The manager must NOT:
- write code as part of routing
- embed skill instructions inline
- duplicate detailed policy that belongs in `AGENTS.md`

---

## 2. Classify Before Action

Before any non-trivial action begins, the manager must explicitly classify:
- complexity
- risk
- whether the task crosses domains or systems

If the task is actually trivial, the manager should say so and release it for direct execution.

---

## 3. Name the Concrete Next Capability

The manager must produce a concrete routing decision.

That decision must identify:
- which workflow, skill, or agent is next
- what validation or review gates apply
- whether any reference docs must be loaded

Ambiguous guidance such as "follow the usual process" is non-compliant.

---

## 4. Append `task-complete` to Every Non-Trivial Pipeline

The manager is responsible for appending `task-complete` as the final step of every non-trivial pipeline at routing time.

Individual workflows or pipelines do NOT declare `task-complete` themselves.
Completion enforcement is centralized in the manager.

---

## 5. Escalate by Risk

The manager must route stronger safeguards for higher-risk work.

Examples:
- low or medium risk non-trivial work: workflow plus validation
- high-risk work: workflow plus review loop
- system-level work: strongest available routing path, potentially including specialized agents

The exact local workflow names may vary by project.
The escalation principle may not.

---

## 6. Stop on Missing Policy

If the routing decision depends on policy that is absent, conflicting, or ambiguous, the manager must not guess.

It must:
- stop
- surface the ambiguity explicitly
- return the task to clarification or brainstorming before execution continues

---

# Output of Manager

At routing time, the manager must produce a short execution plan that includes:
- task classification
- selected capabilities in order
- validation and review requirements
- explicit final `task-complete` step for non-trivial work

The output should be concise, deterministic, and immediately actionable.

---
