---
version: 2.10.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/conventions/traceability.md
---

# traceability.md

## Purpose

This convention defines how instruction systems make non-trivial routed execution auditable in the conversation transcript.

Visible traceability prevents compliance from depending on the agent's memory or private judgment.

## Visible Output Artifacts

Every non-trivial routed step whose result gates a later routed step, validation gate, review gate, documentation maintenance step, or completion step must define and emit a visible output artifact.

This applies to:
- manager-equivalent routing decisions
- skills whose output is consumed by a later non-trivial routed step
- agent reviews used as acceptance gates
- validation steps for non-trivial routed work
- documentation maintenance steps in non-trivial routed work
- task-complete closure

The artifact must be present in the conversation before any downstream capability treats the step as complete.

This convention does not require output artifacts for trivial direct work, exploratory tool use, or intermediate commands inside a single capability.

## Artifact Label

Each emitted artifact must start with a stable, grep-able label:

`Skill: <capability-name> - output below`

Use the correct layer name when the capability is not a skill:
- `Manager: <capability-name> - output below`
- `Agent: <agent-name> - output below`
- `Pipeline: <pipeline-name> - output below`

Project-specific wording may be added after the label, but the label itself must remain recognizable.

## Minimum Artifact Content

An output artifact must include enough structured information for the next routed gate to verify it.

At minimum, include:
- status: completed, skipped, or blocked
- target files, areas, or decisions covered by the routed step
- assumptions or inferred decisions that affected the routed step
- validation, review, or conflict checks performed by the routed step when relevant
- blockers or incomplete work when present

Use a table when the capability checks multiple gates, files, or decisions.

## Raw Tool Output Is Not A Contract

Running commands, tools, searches, or tests directly does not satisfy a non-trivial routed capability output contract by itself.

Raw tool output may be evidence, but the capability must still emit its own artifact summarizing:
- what was run or inspected
- what passed, failed, or remained unverified
- how the result satisfies the capability's declared gate

## Missing Artifact Handling

If a downstream step depends on a capability whose output artifact is missing:
- do not infer success from memory
- do not substitute raw tool output
- return to the missing capability or report the missing artifact as a blocker
