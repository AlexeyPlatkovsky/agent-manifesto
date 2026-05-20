---
version: 2.8.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/protocols/manager.md
implementation: mandatory
requires_when:
  - routing must choose between multiple skills, pipelines, or agents
---

# manager.md

## Purpose

This protocol defines canonical centralized routing behavior for projects that need a manager-equivalent routing capability.

It is a framework input.
Project manager-equivalent routing capabilities derived from it must be standalone project artifacts.

---

# Mandatory Implementation Rules

Any project manager-equivalent routing capability derived from this protocol must:
- stay purely responsible for routing and orchestration
- classify non-trivial work before execution begins
- name the selected existing pipeline or immediate next concrete capability
- name the expected visible output artifact for each non-trivial routed handoff
- require the expected output artifact before advancing across a non-trivial routed handoff
- append documentation maintenance before `task-complete` when its trigger applies
- append `task-complete` to non-trivial routed work
- verify required planned output artifacts before invoking `task-complete`
- escalate safeguards as task risk increases
- stop and surface ambiguity instead of guessing

Projects may adapt the manager-equivalent capability to repository-specific capability names and local pipeline names.

---

# When Manager Applies

The manager-equivalent applies when:
- a task is non-trivial
- routing must choose between multiple skills, pipelines, or agents

It does not apply:
- to trivial tasks
- when the task fits direct execution without routing
- to purely factual questions with no execution path

---

# Core Rules

## 1. Routing Only

The manager selects an existing pipeline or the immediate next capability and required gates.
It does not implement execution steps itself.
It must not invent or inline execution sequences that belong in pipeline files.

## 2. Classify Before Action

Before non-trivial work begins, the manager must explicitly classify:
- complexity
- risk
- whether the task crosses domains or systems

Classification must produce visible output — a stated classification — before any file is created, edited, or deleted. A silent internal check does not satisfy this rule.

When a session begins as discussion or design and the user signals readiness to proceed ("go ahead", "do it", "implement it", "fix it", or equivalent), the manager gate fires again at that moment. The signal is not blanket permission to skip routing.

If the task is actually trivial, the manager must say so and release it for direct execution.

## 3. Name the Concrete Next Capability

The manager must produce a concrete routing decision.

That decision must identify:
- which existing pipeline or immediate next skill/agent is selected
- what validation or review gate applies
- whether reference docs must be loaded
- the expected visible output artifact label for each non-trivial routed handoff

The routing decision itself must be emitted as a visible manager output artifact.

## 4. Check Routed Handoffs

At each non-trivial routed handoff, the manager must inspect the previous step's output artifact and explicitly select the next planned step.

Do not advance across a non-trivial routed handoff when the expected output artifact is absent.

Raw tool output, command success, or a private recollection of work performed does not satisfy a routed handoff's output artifact contract.

Reload the manager-equivalent instructions when the next step is ambiguous, the plan changed, or the conversation context no longer contains the routing plan.

## 5. Centralize Post-Change Documentation Maintenance

When documentation maintenance applies, the manager is responsible for placing it after the substantive project change and before `task-complete`.

The manager must not make execution skills repeat this enforcement rule.

## 6. Centralize Task Completion

The manager is responsible for appending `task-complete` as the final step of non-trivial routed work.

The manager must centralize this responsibility rather than requiring execution skills or pipelines to repeat it.

Before invoking `task-complete`, the manager must verify every required planned output artifact is present in the conversation.

For each required planned artifact, the manager must reference its artifact label or transcript location when the tool exposes one. If any required artifact is missing, return to the missing step or report the missing artifact as a blocker.

## 7. Escalate by Risk

Examples:
- low or medium risk non-trivial work: pipeline plus validation
- high-risk work: pipeline plus stronger review
- system-level work: strongest available routing path

## 8. Stop on Missing Policy

If a safe routing decision depends on missing or conflicting policy:
- stop
- surface the ambiguity
- ask for clarification, or route to brainstorming when its trigger is present and the capability exists

---

# Output Contract

At routing time, produce a short execution plan that includes:
- task classification
- selected existing pipeline or immediate next capability
- validation and review requirements
- documentation maintenance step when its trigger applies
- explicit final `task-complete` step for non-trivial routed work
- expected visible output artifact label for each non-trivial routed handoff

The plan must begin with:

`Manager: <capability-name> - output below`
