---
version: 2.10.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/IMPLEMENTATION.md
---

# IMPLEMENTATION.md

## Purpose

This document defines how the agent-manifest framework realizes the values and principles in [MANIFEST.md](MANIFEST.md).

`MANIFEST.md` states what must be true. `IMPLEMENTATION.md` defines the practices, layers, gates, and file conventions that make those truths operational.

---

# Framework Sources

The framework has six source types:

- `MANIFEST.md` defines values and principles.
- `IMPLEMENTATION.md` defines framework mechanics.
- `conventions/*.md` define shared framework standards used by multiple stages, protocols, or agent templates.
- `NN_name.md` files define framework stages.
- `protocols/*.md` define framework protocols used by stages.
- `agents/*.md`, excluding `agents/_README.md`, define framework agent templates used by generated landscapes.

## Framework Conventions

Framework conventions are shared standards for framework artifacts.

Rules:
- use a convention only when at least two framework artifacts need the same standard
- conventions define standards, not routing, sequencing, validation gates, or execution procedure
- stages, protocols, and agent templates reference conventions instead of restating them
- use one convention file per concern

---

# Framework Stages

A stage is a framework prompt file named with the `NN_name.md` pattern.

Current stages:
- `00_project_profile.md`: create or update `.ai/docs/project_specification.md`
- `01_initial_composition.md`: build the initial instruction system
- `02_review.md`: audit an instruction system for compliance
- `03_capability_expansion.md`: add justified skills, pipelines, agents, conventions, or docs
- `04_tool_adoption.md`: adopt an external tool into an existing instruction system

Stage rules:
- `00_project_profile.md` must run before any other stage
- stages 01-04 must stop if `.ai/docs/project_specification.md` is missing
- stages apply `MANIFEST.md`, `IMPLEMENTATION.md`, framework conventions, framework protocols, applicable agent templates, and the project specification together
- stage files are not project runtime artifacts

## Stage Standards

These standards apply to every stage. Stages declare what is stage-specific without restating these rules.

### Context Required

Every stage must declare a "Context Required" list naming the files it needs.

If any listed file is missing, the stage must stop and ask the user to provide it.

If `.ai/docs/project_specification.md` is missing, stages 01-04 must stop and require `00_project_profile.md` first.

### Brainstorming

When a stage uses brainstorming, cite `protocols/brainstorm.md` and follow it exactly. Do not restate its rules; name only the stage-specific scope and topics.

### Composition Anchor

When a stage enters a composition, implementation, or fix-application phase, it must apply this document's §Project Landscape, §Principle Implementation, §Framework Protocol Contract, §Framework Agent Template Contract, §Capability Triggers, and all relevant `conventions/*.md`. Stage-specific composition rules supplement, not replace, these anchors.

### Phase Discipline

Stages must not modify files during inventory, audit, discovery, discussion, brainstorm, clarification, reconciliation, or proposal phases. File modifications belong only in the stage's composition or implementation phase, and only after explicit user approval.

---

# Project Landscape

Generated or reviewed instruction systems use these layers when justified by the project.

## Project Profile

The project profile is the reusable specification stored at `.ai/docs/project_specification.md`.

Rules:
- it is created or updated by `00_project_profile.md`
- it records the user's role, recurring duties, AI tools, capability triggers, quality expectations, authoritative sources, domain vocabulary, and accepted assumptions
- stages 01-04 must read it before acting
- if it is missing, stages 01-04 must stop and require `00_project_profile.md`
- it is project knowledge, not a behavioral rule

## Root Contract

The root contract is the always-loaded policy layer. It classifies tasks, enforces gates, defines constraints, and routes work. It does not execute task procedures.

Use `conventions/tool-adapters.md` for single-tool and multi-tool root contract models, native entrypoint verification, and thin adapter requirements.

Shared multi-tool storage uses:
- `.ai/agents`
- `.ai/conventions`
- `.ai/docs`
- `.ai/pipelines`
- `.ai/skills`

The framework-standard shared skill format is `.ai/skills/<skill_name>/SKILL.md` using markdown with Claude-style YAML frontmatter. At minimum, the frontmatter must include `name` and `description`.

If a project already stores capabilities elsewhere, migration is a structural refactor and requires user approval.

## Skills

A skill is a reusable capability — a behavior, procedure, or action pattern an agent uses to solve part of a task. A skill runs in the main agent's working context, shares that context, and may interact with the user as the work proceeds.

Rules:
- one responsibility
- runs in the working context; may interact with the user mid-task
- no orchestration logic
- no cross-skill routing
- no duplicated root policy
- standalone project-local behavior
- a visible output contract when the skill's result gates another step in non-trivial routed work

## Pipelines

Pipelines are ordered orchestration for non-trivial work.

Rules:
- pure sequencing only
- reference skills or agents
- do not redefine skill behavior
- include validation for non-trivial work
- require each non-trivial routed handoff's visible output artifact before the next step treats it as complete
- use one file per pipeline when more than one pipeline exists or when a pipeline is substantial
- create a pipeline when a repeated task type is non-trivial and has a distinct ordered execution path
- do not collapse distinct workflows into one generic pipeline when their steps, validation, or review gates differ

For software projects, common pipeline candidates include feature implementation, code review, and code refactoring. Create these only when the project profile or repository evidence shows they are real recurring work, but explicitly evaluate whether they are needed during initial composition for software repositories.

## Agents

An agent is a responsible actor with a clearly defined input and output that runs in an isolated context. An agent does not share the main conversation's context and does not hold multi-turn dialogue with the user; it receives its input, runs to completion, and returns its result.

Rules:
- runs in an isolated context with a defined input and output
- runs to completion without live, multi-turn user interaction
- do not create a default agent layer without evidence of need
- mandatory framework agent templates with a present `requires_when` trigger are evidence of need
- keep agent responsibilities distinct from skills and pipelines
- use agents for isolation, an independent unbiased pass, or parallel responsibility, not decoration
- copy mandatory framework agent templates into every generated landscape where their trigger applies
- preserve the template's responsibility and output contract when adapting to a tool-specific agent format
- use the artifact acceptance tester after materially changing runtime instruction artifacts and before accepting them

## Skill Versus Agent

A skill and an agent are different kinds of execution capability, distinguished by context locality. Which one a capability is must be decided deliberately whenever an execution capability is created or audited.

Apply `conventions/skill-vs-agent.md`.

## Conventions

Conventions are mandatory shared standards used by multiple skills or agents.

Rules:
- create a convention only when at least two skills or agents need the same behavior
- never create a convention for one skill only
- define how to approach a category of work, not how to perform one task
- do not classify, route, sequence, or execute work
- skills and agents reference conventions instead of copying them
- in multi-tool or AI-agnostic projects, store shared conventions under `.ai/conventions`
- use one file per convention area, such as `.ai/conventions/code.md` or `.ai/conventions/testing.md`
- a referenced convention is mandatory for the referencing skill or agent

Shared conventions prevent drift; consistency across skills follows automatically.

## Reference Docs

Reference docs hold reusable project knowledge.

Rules:
- use docs for facts such as architecture, commands, domain context, and repository structure
- structure docs for selective loading with `.ai/docs/README.md`, purposeful subfolders, and stable section targets
- keep docs on demand, not always loaded
- docs inform but do not enforce behavior

Apply `conventions/reference-docs.md`.

## Traceability

Routed execution must be auditable from visible conversation artifacts, not inferred from private agent state.

Apply `conventions/traceability.md`.

## Layer Purity

Every artifact must stay inside the responsibility boundary of its layer.

Apply `conventions/layer-purity.md`.

If a layer is about to absorb content that belongs elsewhere, place the content in the correct layer first. A pipeline whose body could be deleted without losing execution detail because the detail lives only there is a skill mislabeled as a pipeline.

---

# Principle Implementation

## Context And Simplicity

### 1. Load Only What You Need

Implementation:
- keep the root contract small and policy-focused
- load skills, pipelines, agents, conventions, and docs only when relevant
- avoid placing task-specific instructions in always-loaded files
- split large instruction files when they are large because they have multiple jobs

The 150-line target remains a strong guideline for generated project instruction files, not a hard cap. Do not sacrifice clarity, correctness, or single responsibility just to satisfy the target.

### 2. Earn Complexity

Implementation:
- create only artifacts the current project actually needs
- reuse good existing project capabilities before adding new ones
- preserve existing naming when it is already coherent
- add configurability only when the current project requires it
- generalize only after a repeated pattern exists

Classify work by complexity and risk.

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

Translate this matrix into mandatory gate language in the root contract. Do not copy the matrix itself into generated root contracts.

## Authority And Structure

### 3. One Artifact, One Job

Implementation:
- root contract: policy and routing gates
- skill: reusable capability run in the main agent's working context
- pipeline: ordered orchestration
- agent: responsible actor with a defined input and output run in an isolated context
- convention: shared standard
- reference doc: reusable project knowledge

Skills and agents are distinguished by context locality, not by how much they reason. Apply `conventions/skill-vs-agent.md`.

If a file grows because it is doing too many jobs, split it rather than expanding it indefinitely.

Decision and execution boundaries:
- put classification, routing gates, constraints, and required outputs in the root contract
- put task procedures in skills, which run in the working context
- put sequencing in pipelines
- put isolated-context, defined-input-and-output responsibilities in agents
- keep project knowledge in docs and shared standards in conventions

Execution skills must not contain manager handoff text, stage metadata, or routing to other skills.

### 4. One Owner Per Concern

Implementation:
- centralize each behavioral requirement in the layer responsible for it
- reference conventions and docs instead of copying their text into skills or agents
- derive project capabilities from framework protocol metadata, not from memorized protocol names
- do not let project skills depend on framework protocol files or framework-only paths at runtime

If an existing project capability exactly satisfies a required capability, reuse it.

An exact match means:
- the responsibility matches
- required framework protocol coverage matches
- no contradiction with the framework exists

If an existing capability is only close:
- treat it as non-equivalent
- stop and ask the user whether to split, preserve, replace, or create another artifact

Use the project's existing capability names when they already satisfy the framework. Do not create a near-duplicate capability just to match a canonical protocol filename.

If a project-native name fulfills a protocol:
- keep the project-native name
- note the protocol mapping once in the root contract or review report

If the naming convention is unclear or conflicts with framework defaults, ask the user.

## Control And Safety

### 5. Make Behavior Explicit

Before non-trivial implementation:
- state assumptions explicitly
- surface ambiguity instead of guessing
- define success criteria
- name intended verification

Avoid descriptive routing without a stop gate, implied validation, and implied completion behavior.

Gate behavior:
- for non-trivial tasks, the root contract must use imperative blocking language
- routing gates must appear before the capability registry

Compliant pattern:
- classify the task first
- if trivial: proceed directly and state the classification
- if non-trivial: stop, load the concrete routing capability, and do not implement until routing resolves
- loading the routing capability is not enough; non-trivial work may begin only after the routing capability emits its visible output artifact
- if unsure: treat as non-trivial
- classification must be stated out loud before any file is created, edited, or deleted; a silent mental check does not satisfy the gate
- when a conversation begins as discussion or design and the user signals to proceed ("go ahead", "do it", "implement it", "fix it", or equivalent), treat that signal as a fresh routing gate trigger, not as permission to skip classification

Validation is mandatory for non-trivial routed work:
- every non-trivial pipeline must include at least one explicit validation step
- stronger review loops apply only for higher-risk work
- validation should be automated and repeatable where possible
- validation is a required check unless a project explicitly creates a concrete validation skill, pipeline step, or convention
- raw command output does not satisfy a validation gate unless the validation capability emits its visible output artifact
- validation artifacts must state pass, fail, skipped, or blocked for each declared validation gate
- `task-complete` is the required closure skill for non-trivial routed work
- `task-complete` enforcement should be centralized in the root contract or manager-equivalent artifact, not repeated across execution skills

### 6. Ask Before You Cut

If compliance or implementation requires a risky change, stop and ask the user before changing it.

Risky changes include:
- moving capabilities to a new directory
- splitting a monolithic file
- merging or deleting duplicated artifacts
- renaming or replacing existing capabilities
- choosing between multiple valid implementation contracts

When asking, explain:
- what should change
- why the change is needed
- what the safe target state would be

---

# Framework Protocol Contract

Protocols in `protocols/` are canonical framework inputs. They are not project runtime files.

Every protocol must follow `conventions/framework-metadata.md`.

Each protocol body must define:
- purpose
- mandatory rules that implementations must preserve
- allowed project-specific adaptations
- output contracts, when other capabilities or validation depend on this one's result

Output contracts that gate downstream non-trivial routed work must follow `conventions/traceability.md`.

## Capability Derivation

Apply `conventions/capability-derivation.md`.

---

# Framework Agent Template Contract

Agent templates in `agents/`, excluding `agents/_README.md`, are canonical framework inputs for specialized project-local agents.

Every agent template must follow `conventions/framework-metadata.md`.

Apply `conventions/capability-derivation.md` for agent template derivation and generated project agent requirements.

---

# Capability Triggers

Prefer the smallest coherent system that satisfies the triggers actually present in the project profile and repository evidence.

Use these triggers:
- any AI landscape: instruction-evaluator agent
- new or materially changed skills, pipelines, agents, manager-equivalent routing, validation gates, or output contracts: artifact-acceptance-tester agent
- multiple AI tools or AI-agnostic portability need: root contract plus thin adapters
- open design decisions or setup/profile clarification choices with trade-offs: brainstorming capability
- non-trivial routed work: explicit validation check and task-complete capability
- feature implementation, refactoring, or non-trivial bug fix that changes project behavior, structure, commands, contracts, workflows, domain facts, or known failure modes: documentation maintenance capability
- routing must choose between multiple skills, pipelines, or agents: manager-equivalent capability
- repeated multi-step workflow or repeated non-trivial task type with distinct steps: pipeline
- repeated task type that runs in the working context: skill (apply `conventions/skill-vs-agent.md`)
- repeated behavior across skills or agents: project convention
- reusable project facts such as architecture, commands, domain vocabulary, or source locations: reference doc
- isolated-context work with a defined input and output, or an independent unbiased pass: agent (apply `conventions/skill-vs-agent.md`)
- high-risk or system-level work: stronger review and validation gates

Do not create managers, pipelines, agents, conventions, or docs by default. Create them only when a concrete trigger exists.

---

# Final Rule

Reject, defer, or redesign any proposed change that:
- adds unnecessary always-loaded context
- duplicates an existing source of truth
- creates a competing authority
- introduces orchestration where direct execution would suffice
- forces a risky change without user approval
