---
version: 1.5.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/protocols/manager.md
implementation: mandatory
applies_to:
  - medium
  - large
---

# manager.md

## Purpose

This protocol defines canonical centralized routing behavior for medium and large projects.

It is a framework input.
Project skills derived from it must be standalone project artifacts.

---

# Mandatory Implementation Rules

Any project skill derived from this protocol must:
- stay purely responsible for routing and orchestration
- classify non-trivial work before execution begins
- name the next concrete capability or capabilities
- append `task-complete` to every non-trivial pipeline
- escalate safeguards as task risk increases
- stop and surface ambiguity instead of guessing

Projects may adapt the skill to repository-specific capability names and local pipeline names.

---

# When Manager Applies

The manager-equivalent applies when:
- the project is medium or large
- a task is non-trivial
- routing must choose between multiple skills, pipelines, or agents
- validation and completion enforcement should stay centralized

It does not apply:
- to trivial tasks
- to small projects that still fit direct routing
- to purely factual questions with no execution path

---

# Core Rules

## 1. Routing Only

The manager chooses and sequences capabilities.
It does not implement execution steps itself.

## 2. Classify Before Action

Before non-trivial work begins, the manager must explicitly classify:
- complexity
- risk
- whether the task crosses domains or systems

If the task is actually trivial, the manager should say so and release it for direct execution.

## 3. Name the Concrete Next Capability

The manager must produce a concrete routing decision.

That decision must identify:
- which skill, pipeline, or agent is next
- what validation or review gate applies
- whether reference docs must be loaded

## 4. Centralize Task Completion

The manager is responsible for appending `task-complete` as the final step of every non-trivial pipeline.

Execution skills and pipelines should not repeat that responsibility.

## 5. Escalate by Risk

Examples:
- low or medium risk non-trivial work: pipeline plus validation
- high-risk work: pipeline plus stronger review
- system-level work: strongest available routing path

## 6. Stop on Missing Policy

If a safe routing decision depends on missing or conflicting policy:
- stop
- surface the ambiguity
- return for clarification or brainstorming before execution continues

---

# Output Contract

At routing time, produce a short execution plan that includes:
- task classification
- selected capabilities in order
- validation and review requirements
- explicit final `task-complete` step for non-trivial work
