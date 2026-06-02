---
version: 2.10.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/01_initial_composition.md
---

# 01_initial_composition.md — Initial Composition

## Context Required

Before starting, ensure the following files are available in this session:
- `MANIFEST.md`
- `IMPLEMENTATION.md`
- all framework convention files under `conventions/`
- `protocols/_README.md`
- all canonical protocol files under `protocols/`, excluding `protocols/_README.md`
- all canonical agent template files under `agents/`, excluding `agents/_README.md`
- `.ai/docs/project_specification.md`

If `.ai/docs/project_specification.md` is missing, stop and require `00_project_profile.md` first.

If any framework source is missing, stop and ask the user to provide it.

Use `protocols/_README.md` only as an inventory index. Derive capabilities using `conventions/capability-derivation.md`.

---

## Purpose

Create or adjust the smallest coherent AI instruction system that fully aligns with `MANIFEST.md` and `IMPLEMENTATION.md`.

The result must be correct enough to stand on its own.
`02_review.md` may catch bugs, but it is not the planned repair phase for an intentionally rough draft.

You must also:
- use `.ai/docs/project_specification.md` as the authoritative profile source
- ask only for profile clarification when the profile has gaps that block composition
- keep generated project capabilities standalone and project-local

---

## Working Mode

Work in exactly 3 phases:
1. Inventory
2. Discussion
3. Composition

During Discussion, use `protocols/brainstorm.md` as the governing protocol for high-impact design choices.
During Composition, do not return to Phase 2 brainstorming unless a new high-impact design decision is discovered. Pause only for explicit approval or clarification gates required by `IMPLEMENTATION.md`.

---

## Phase 1 — Inventory

Investigate the repository before proposing any changes.

Read `.ai/docs/project_specification.md` first. Treat it as the authoritative source for user role, recurring duties, capability triggers, AI tools, quality expectations, and local authority sources unless the repository clearly contradicts it.

### A. Project Nature

- what kind of project is this
- likely capability triggers
- maturity: prototype, active development, stable, or legacy
- single-purpose or multi-domain

### B. Tech Stack

- languages and frameworks
- test stack
- build and CI tooling
- runtime or deployment environment

### C. Existing Documentation

- root docs
- architecture or design docs
- conventions docs
- pipeline docs
- existing AI instruction files
- duplicated or conflicting guidance

### D. Existing Instruction System

- what acts as the current root operational contract
- whether `AGENTS.md` exists
- whether native tool entrypoints exist
- whether skills, pipelines, agents, or reference docs already exist
- whether shared project conventions already exist
- whether routing logic exists
- whether execution skills are improperly coupled to orchestration

### E. AI Tool Surface

- which AI tools are already configured or clearly intended
- which tool-specific entry files exist
- whether the repo is single-tool or multi-tool
- whether existing tool-specific files contain real policy or are already adapters
- whether any tool-specific adapter is too passive to enforce the root contract

### F. Reusable Project Knowledge

Identify reusable knowledge that may justify reference docs:
- architecture
- commands
- domain context
- repository structure

Identify repeated behavior that may justify shared project conventions:
- coding standards
- work standards
- testing standards
- domain standards

Identify repeated non-trivial task types that may justify pipelines.

For each candidate, classify provisionally whether it is:
- a direct task that needs no pipeline
- a skill that runs in the working context
- an agent that runs in an isolated context with a defined input and output
- a pipeline with distinct ordered steps, validation, or review gates

For any execution candidate, note provisionally whether it is a skill or an agent per `conventions/skill-vs-agent.md`.

Do not decide what to create yet.

### G. Protocol Inventory

- read every canonical protocol under `protocols/`, excluding `protocols/_README.md`
- apply `conventions/framework-metadata.md`
- determine which protocol triggers are present
- determine which optional protocols may be justified by project needs and present triggers
- identify any cross-capability enforcement declared by the protocols

### H. Agent Template Inventory

- read every canonical agent template under `agents/`, excluding `agents/_README.md`
- apply `conventions/framework-metadata.md`
- determine which agent template triggers are present
- identify mandatory framework agents that must be copied into the generated AI landscape

### I. Structural Risk Inventory

Explicitly identify:
- duplicated skills or near-duplicate names
- monolithic pipeline registries that would need splitting
- existing capabilities that may already satisfy a required protocol
- any risky change that would require user approval before implementation

---

## Phase 1 Output

Stop after inventory and provide:
1. project summary
2. current instruction-system summary
3. initial compliance check
4. main risks, gaps, and ambiguities
5. proposed discussion agenda

End with an explicit checkpoint:
- say Phase 1 is complete
- ask the user to confirm or correct the inventory
- state that Phase 2 will begin only after confirmation
- do not ask the first discussion question in the same message

Do not edit or create files in Phase 1.

---

## Phase 2 — Discussion

Resolve only the high-impact decisions identified in Phase 1.

Follow `protocols/brainstorm.md` for question format, stopping behavior, decision summary, and confirmation.

Ask only what is actually needed to complete a correct design. Do not repeat profile questions that `.ai/docs/project_specification.md` already answers.

High-impact discussion topics may include:
- contradictions between the profile and repository evidence
- primary AI landscape when the repo mixes tools
- single-tool versus multi-tool or AI-agnostic structure
- where instruction artifacts should live
- whether existing capabilities exactly satisfy required protocol-derived capabilities
- whether pipelines are justified and which real pipeline should be formalized first
- whether reference docs should be created
- whether shared project conventions are justified by repeated behavior across skills or agents
- whether existing files should be migrated, split, merged, or preserved
- whether unselected AI entry files should be removed or neutralized

At the end of discussion:
- produce a decision summary
- ask the user to confirm it before Phase 3

---

## Phase 3 — Composition

Begin only after the user confirms the decision summary.

### Composition Rules

Apply `IMPLEMENTATION.md` §Stage Standards §Composition Anchor, plus §Capability Triggers for this stage.

Stage-specific reminders:
- verify the chosen tool's native entrypoint convention against current official docs during composition; if current official docs cannot be accessed or the entrypoint cannot be verified, stop and ask the user for an authoritative source or approval to defer that tool-specific composition
- before writing any execution capability, classify it explicitly as a skill or an agent per `conventions/skill-vs-agent.md`, and state the decision and its justification out loud before creating the file
- use `pipeline` terminology consistently
- apply `conventions/tool-adapters.md` to every tool-specific entry file
- if repeated software task types such as feature implementation, task review, or anything else have distinct ordered steps, create separate pipelines for them instead of representing them only as skills
- before any risky change (splitting monolithic files, moving artifacts into `.ai/`, renaming, merging, deleting, replacing tool entrypoints, choosing between multiple valid implementation contracts), stop and ask the user — name what changes, why, and the compliant target state
- if composition uncovers a new high-impact design decision, stop composition, report the blocker, reopen Phase 2 discussion under `protocols/brainstorm.md`, and resume composition only after a confirmed decision summary

### Layer Purity

Apply `conventions/layer-purity.md` to every file written in this stage.

### Traceability

Apply `conventions/traceability.md` to generated non-trivial routed handoffs, manager-equivalents, validation gates, documentation maintenance capabilities, acceptance-review agents, and completion capabilities.

### Skill Extraction Precondition For Pipelines

A pipeline may not be written until the skills it sequences exist or are scheduled for creation in the same composition.

Before authoring any pipeline:
1. list the atomic operations it sequences
2. resolve each operation to one of: an existing skill, a new skill to create in this composition, or a single trivial command (one line, no procedure)
3. if an operation needs more than a one-liner and is not yet a skill, create the skill before writing the pipeline

If this precondition cannot be met, the capability is not yet a pipeline — keep it as a skill or pause and ask the user.

### Protocol-Derived Capabilities

Derive required capabilities from protocol frontmatter per `conventions/capability-derivation.md`.

Use the protocol filename basename as the default capability name only when the project does not already have an exact equivalent. An existing capability is exact only when responsibility matches, mandatory protocol coverage matches, and no contradiction exists. If only close, treat as non-equivalent and ask the user before splitting, merging, replacing, or duplicating.

### Agent-Template-Derived Capabilities

Derive required project-local agents from agent template frontmatter per `conventions/capability-derivation.md`.

### Instruction Artifact Acceptance

Before final acceptance, verify the project-local instruction-evaluator and artifact-acceptance-tester agents exist when their triggers apply.

Use `instruction-evaluator` to review new or changed instruction artifacts.
Use `artifact-acceptance-tester` to run 9 scenario tests for each new or materially changed skill, pipeline, agent, manager-equivalent routing artifact, validation gate, or output contract.

### Scope Boundaries

If multiple AI tools are detected but the user selected only some of them:
- update only the selected tools
- do not silently rewrite unselected tool entrypoints
- if stale unselected tool files remain, ask whether to remove or neutralize them

---

## Final Output Format

When composition is complete, provide:

### 1. Final Assessment
- what was found
- what was wrong or missing
- what decisions were made

### 2. Target Architecture
- what files now exist
- what each file is responsible for

### 3. Change Summary
- what was created
- what was updated
- what was removed or merged

### 4. Remaining Trade-Offs
- what is intentionally kept simple
- what can be added later if the project grows

### 5. Validation Performed
- concrete checks completed
- checks skipped or deferred, with reason
- residual risks, if any

---

## Quality Bar

The final system must:
- align with `MANIFEST.md`
- align with `IMPLEMENTATION.md`
- be project-specific rather than generic
- stand on its own without requiring `02_review.md` to rescue obvious flaws
- avoid duplicated conventions
- avoid competing authorities
- avoid unnecessary abstraction
- preserve good existing project capabilities where possible
- keep routing centralized in the root contract or manager-equivalent artifact
- pass `conventions/layer-purity.md`
- pass instruction artifact evaluation and acceptance testing when their triggers apply
- contain no pipeline whose skills do not yet exist
