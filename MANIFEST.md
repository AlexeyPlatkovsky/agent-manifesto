---
version: 1.4.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/MANIFEST.md
---

# MANIFEST.md

## Purpose

This document defines the canonical rules for designing, reviewing, and evolving AI instruction systems.

It is framework-level guidance.
It is not part of the generated project runtime.

The framework exists to answer one question:

> How should an AI instruction system stay minimal, predictable, and scalable without wasting context?

---

# Core Principles

## 1. Minimize Always-Loaded Context

Only the minimum required root contract should be always loaded.

Everything else must be:
- modular
- on-demand
- explicitly invoked

## 2. Separate Policy from Execution

Policy defines:
- classification
- routing gates
- constraints
- required outputs

Execution defines:
- how a skill performs a task
- how a pipeline sequences capabilities

Policy lives in the root contract:
- `AGENTS.md` for multi-tool or AI-agnostic projects
- the tool's native entrypoint for single-tool projects

Execution lives in:
- skills
- pipelines
- agents

## 3. Progressive Disclosure of Complexity

Escalate only when needed:
1. direct execution
2. skill-based execution
3. pipeline-based execution
4. agents or subagents

Never begin at level 4 by default.

## 4. No Duplication

Any rule should exist only once.

Allowed:
- referencing a rule
- centralizing a rule in the correct layer

Forbidden:
- repeating routing policy in skills
- repeating validation rules across multiple artifacts
- copying the same execution instructions into both a skill and a pipeline

## 5. Explicit Responsibility Boundaries

Each file should have one responsibility.

Examples:
- root contract: policy and routing gates
- manager-equivalent: routing and orchestration only
- execution skill: task execution only
- pipeline: ordered orchestration only
- reference doc: reusable project knowledge only

Execution skills must stay isolated.
They must not contain manager handoff text, stage metadata, or routing to other skills.

## 6. Deterministic Over Implicit

Critical behavior must be explicit.

Avoid:
- "AI will figure it out"
- descriptive routing without a stop gate
- implied validation or completion behavior

## 7. Optimize for Real Projects

Do not build for a future the repository does not justify.

Prefer:
- reusing good existing project capabilities
- preserving existing naming when it is already coherent
- creating only artifacts the current project actually needs

## 8. Routing Rules Must Be Mandatory Gates

For non-trivial tasks, the root contract must use imperative blocking language.

Compliant pattern:
- classify the task first
- if trivial: proceed directly and state the classification
- if non-trivial: STOP, load the concrete routing capability, and do not implement until routing resolves
- if unsure: treat as non-trivial

Routing gates must appear before the capability registry.

## 9. Keep Instruction Files Compact

Every instruction file should target 150 lines or fewer when possible.

This is a strong target, not a hard cap.
Do not sacrifice clarity, correctness, or single responsibility just to force the file under the line limit.

If a file grows because it is doing too many jobs, split it rather than letting it expand indefinitely.

## 10. Ask Before Structural Refactors

If compliance requires a structural refactor, stop and ask the user before changing it.

Structural refactors include:
- moving capabilities to a new directory
- splitting a monolithic file
- merging or deleting duplicated artifacts
- renaming or replacing existing capabilities

When asking, explain:
- what should change
- why the current structure violates the framework
- what the target structure would be


---

# Root Contract Rules

## Single-Tool Projects

If a project supports only one AI tool, the project's full operational contract may live directly in that tool's official native entrypoint file.

Rules:
- the native entrypoint must be verified against the tool's current official documentation during composition
- the native entrypoint becomes the project's root operational contract
- supporting artifacts should use the selected tool's native structure by default
- `AGENTS.md` is not required in this mode

## Multi-Tool or AI-Agnostic Projects

If a project supports multiple AI tools, or the user explicitly wants an AI-agnostic structure:
- `AGENTS.md` is the canonical root operational contract
- every supported tool-specific entry file must be a thin adapter
- each adapter must instruct the tool to follow `AGENTS.md` strictly
- no tool-specific file may become a second source of truth

For shared storage in this mode, use:
- `.ai/skills`
- `.ai/pipelines`
- `.ai/agents`
- `.ai/docs`

If a project already stores capabilities elsewhere, migration is a structural refactor and requires user approval.

---

# Existing Project Adaptation Rules

## Reuse Before Creating

If an existing project capability exactly satisfies a required capability, reuse it instead of creating a new one.

An exact match means:
- the responsibility matches
- the mandatory protocol coverage matches
- there is no contradiction with the framework

If an existing capability is only close:
- treat it as non-equivalent
- stop and ask the user whether to split, preserve, or replace it

## Preserve Project Naming

Use the project's existing capability names when they already satisfy the framework.

Do not create a second near-duplicate capability just to match a canonical protocol filename.

If a project-native name fulfills a protocol:
- keep the project-native name
- note the protocol mapping once in the root contract or review report

If the naming convention is unclear or conflicts with framework defaults, ask the user.

---

# Protocol Contract

Protocols in `protocols/` are canonical framework inputs.
They are not project runtime files.

Project skills must be generated from protocol requirements.
They must not depend on protocol files or framework paths at runtime.

Every protocol must declare structured frontmatter:
- `implementation: mandatory | optional`
- `applies_to: [small, medium, large]`

Protocol frontmatter is authoritative for derivation and review.
Prompt logic must not infer applicability from prose when metadata is present.

Each protocol body must still define:
- purpose
- mandatory rules that implementations must preserve
- allowed project-specific adaptations
- output contracts, when applicable

---

# Protocol-Derived Capability Rules

Capability derivation must come from canonical protocol metadata, not from memorized protocol names or hardcoded prompt logic.

Rules:
- only protocols applicable to the confirmed project size may require implementation
- `protocols/_README.md` is informational and must not participate in capability derivation
- protocols marked `implementation: mandatory` define required project capabilities for applicable project sizes
- protocols marked `implementation: optional` may be implemented only when the project genuinely needs them

Generated project skills must:
- be standalone project artifacts
- include the protocol's mandatory behavior
- include minimal project-specific adaptation
- avoid references to framework files, protocol files, or framework-only paths

---

# Canonical Layers

## Skills

Skills are atomic execution capabilities.

Rules:
- one responsibility
- no orchestration logic
- no cross-skill routing
- no duplicated root policy

## Pipelines

Pipelines are ordered orchestration for non-trivial work.

Rules:
- pure sequencing only
- reference skills or agents
- do not redefine skill behavior
- for medium and large projects, use one pipeline per file

## Agents

Agents are specialized roles used only when context isolation or specialized reasoning is clearly justified by the repository.

Do not create a default agent layer without evidence of need.

## Reference Docs

Reference docs hold reusable project knowledge referenced by multiple skills or pipelines.

They must not be always loaded.

---

# Task Classification Model

Complexity:
- trivial
- non-trivial

Risk:
- low
- medium
- high
- system-level

Execution expectation:
- trivial + low risk: direct execution
- non-trivial + low or medium risk: pipeline plus validation
- non-trivial + high risk: pipeline plus stronger review
- system-level: strongest available routing path

This matrix is not a table to copy into the root contract.
The root contract must translate it into mandatory gate language.

---

# Validation and Completion

Validation is mandatory for non-trivial work.

Rules:
- every non-trivial pipeline must include at least one explicit validation step
- stronger review loops apply only for higher-risk work
- validation should be automated and repeatable where possible

`task-complete` is the required closure skill for non-trivial work.
Its enforcement should be centralized in the routing layer, not repeated across execution skills.

---

# Project Size Guidelines

## Small

Prefer the smallest coherent system.

Defaults:
- no reference docs by default
- no manager by default
- no agents by default
- no pipelines by default unless the project clearly justifies them
- mandatory skills from applicable protocols still apply

## Medium

Must include:
- protocol-derived mandatory skills
- a manager-equivalent routing capability
- at least one pipeline
- explicit validation for every non-trivial pipeline
- reference docs: `architecture.md`, `conventions.md`, `commands.md`

Additional docs may be added when reusable project knowledge justifies them.
Agents should be added only where the repository shows a clear need for context isolation or specialized roles.

## Large

Must include:
- protocol-derived mandatory skills
- a manager-equivalent routing capability
- pipelines
- risk-based routing
- explicit validation for every non-trivial pipeline
- reference docs: `architecture.md`, `conventions.md`, `commands.md`

Agents should be added only where the repository shows a clear need for context isolation or specialized roles.

---

# Final Rule

If a proposed change:
- adds unnecessary always-loaded context
- duplicates an existing rule
- introduces orchestration where direct execution would suffice
- or forces a structural refactor without user approval

then it must be rejected, deferred, or redesigned.
