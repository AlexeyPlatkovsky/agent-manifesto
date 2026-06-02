---
version: 2.10.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/conventions/layer-purity.md
---

# layer-purity.md

## Purpose

This convention defines responsibility boundaries for instruction-system artifacts.

## Layer Tests

- Root contract body: policy, constraints, classification, routing gates, and required outputs only; no execution bodies.
- Manager-equivalent body: routing and gates only; no execution bodies.
- Pipeline body: ordered references to skills, agents, or single trivial commands; no embedded execution procedure, no "how to" prose, no standards, no DSL or coding rules, no checklists that belong in a skill or convention.
- Skill body: one atomic execution capability that runs in the main agent's working context and may interact with the user; may cite conventions and reference docs, but does not sequence sibling skills and does not restate standards already owned by a convention.
- Agent body: a responsible actor with a defined input and output that runs in an isolated context and to completion without live user interaction; no duplicated root policy, convention text, or pipeline sequencing.
- Convention body: shared standards only; no classification, routing, sequencing, validation gates, or task procedure.
- Traceability convention body: shared artifact and transcript standards only; no routing decisions or execution procedure.
- Reference doc body: reusable facts only; no binding behavior.

## Failure Signals

Flag cross-layer leakage when:
- one artifact mixes policy, procedure, sequencing, and reference facts
- a pipeline could be deleted without losing execution detail because the detail lives only there
- a pipeline references skills that do not exist
- a pipeline or skill restates content already owned by a convention or reference doc
- a project has pipelines but an empty or near-empty skill layer

Choosing whether a capability should be a skill or an agent is owned by `conventions/skill-vs-agent.md`; these tests cover only whether each artifact stays inside its own layer.
