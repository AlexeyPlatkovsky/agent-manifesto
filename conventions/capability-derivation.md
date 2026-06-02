---
version: 2.10.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/conventions/capability-derivation.md
---

# capability-derivation.md

## Purpose

This convention defines how framework protocols and agent templates derive project-local capabilities.

## Protocol Derivation

Capability derivation must come from canonical protocol metadata.

Rules:
- only protocols whose `requires_when` trigger is present may require implementation
- `protocols/_README.md` is an index of available protocols and must not participate in capability derivation
- protocols marked `implementation: mandatory` define required project capabilities when their trigger is present
- protocols marked `implementation: optional` may be implemented only when their trigger is present and the project genuinely needs them

Generated project capabilities derived from protocols must:
- be standalone project artifacts
- include the protocol's mandatory behavior
- include minimal project-specific adaptation
- define and emit any visible output artifact required by the protocol or by `conventions/traceability.md` for non-trivial routed work
- avoid references to framework files, protocol files, or framework-only paths

When a protocol derives a skill in a multi-tool or AI-agnostic project, use the framework-standard skill format. When a protocol derives a manager-equivalent routing capability, keep it as a standalone routing artifact, not a skill.

A derived execution capability must be placed as a skill or an agent per `conventions/skill-vs-agent.md`. Decide from context locality, not from the protocol or template filename; the filename does not determine whether the capability runs in the working context or in isolation.

## Agent Template Derivation

Rules:
- templates marked `implementation: mandatory` define required project-local agents when their `requires_when` trigger is present
- templates marked `implementation: optional` may be copied only when their trigger is present and the project genuinely needs them
- `any AI landscape` is the trigger for agents that must be included in every generated project instruction system
- copied agents must remain on demand; root contracts and adapters route to them but do not inline their full instructions
- copied mandatory agents must preserve the template content verbatim when the generated landscape ships the same authority files the template references
- if the generated landscape does not ship the framework authority files, adapt those references to equivalent project-local authority while preserving the template's role, constraints, and output contract
- target-tool formatting may be adapted only as much as needed to make the agent usable in that AI landscape
- generated project agents must avoid references to framework files, template files, or framework-only paths unless those files are intentionally shipped as project-local authority
