---
version: 3.0.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/MANIFEST.md
---

# Agent Manifesto

## Purpose

Agent Manifesto helps a user create, review, or adjust a lightweight AI landscape: a soft harness that gives capable
models the context, boundaries, and reusable structure they cannot reliably infer for themselves.

The framework must improve the user's work without making the user operate the framework.

---

## Values

The framework values:

- useful context over comprehensive prompting
- clear outcomes over prescribed reasoning
- direct work over automatic orchestration
- native tool behavior over simulated machinery
- mechanical guarantees over behavioral reminders
- current evidence over accumulated scaffolding
- user authority over autonomous expansion

The items on the right still matter, but the items on the left matter more.

---

## Landscape Model

Every concern has one natural home:

- **Facts and preferences belong to context.**
- **Universal authority limits belong to the root contract.**
- **Task-scoped policies belong to skills.**
- **Procedures and sequence belong to workflows.**
- **Fresh-context responsibilities belong to agents.**
- **Data shapes belong to contracts.**
- **Reasoning belongs to the model.**
- **Hard guarantees belong to deterministic enforcement.**

An artifact must not absorb a concern that has a better home.

---

## Principles

### 1. Supply What The Model Cannot Know

Record business facts, project realities, user preferences, authoritative sources, and explicit authority boundaries.
Do not explain general practices a capable current model already understands.

Ask of every instruction:

> Would a better model make this unnecessary?

If yes, treat it as temporary scaffolding and require evidence for keeping it. If no, preserve it as durable context,
policy, or authority.

### 2. Keep The Default Context Small

Always-loaded files are a starting brief and map. Load task policies, procedures, specialist responsibilities, and
detailed facts only when relevant.

Splitting a large file does not reduce context when every part is still loaded at startup.

### 3. Describe Outcomes And Boundaries

Tell the model what must be true, what must not happen, and what evidence matters. Leave local reasoning and
implementation choices to the model unless a project-specific fact or risk requires a constraint.

Methodologies such as SDD or TDD express the user's preferred direction and invariants. They are not invitations to
teach the model a generic step-by-step reasoning script.

### 4. Earn Every Artifact

Create a skill, workflow, agent, contract, context file, or adapter only for a present need.

- repeated task-scoped policy can justify a skill
- repeated ordered work can justify a workflow
- a recurring responsibility that materially benefits from fresh context can justify an agent
- a structured boundary that consumers must validate can justify a contract

Do not create empty layers or speculative capability libraries.

### 5. Use Native Capabilities

Prefer each selected tool's current instruction discovery, skills, agents, permissions, hooks, and configuration
mechanisms. Portability means preserving the same intent across native representations, not forcing every tool into one
fictional runtime.

### 6. Enforce What Must Never Drift

Prompt instructions influence behavior; they do not guarantee it. Put non-negotiable restrictions and repeatable
validation in permissions, hooks, schemas, tests, linters, or other deterministic controls when the selected tool makes
that possible.

### 7. Preserve User Authority

Ask before destructive, external, costly, or authority-expanding actions. Consent is scoped to the action approved.

Do not infer permission to commit, push, deploy, publish, contact people, change production, expose data, or restructure
the user's landscape.

### 8. Retest The Harness

Models and tools change. After a significant change, or at least every six months, compare the active landscape with a
fresh minimal baseline on representative work. Preserve durable context and proven guardrails; keep model-compensation
scaffolding only while current evidence shows that it still helps.

The framework is maintained by subtraction as well as addition.

---

## Final Test

A proper landscape lets the user describe the work in ordinary language while the system quietly supplies relevant
context, policy, procedure, isolation, contracts, and enforcement.

If operating the landscape becomes a second job, simplify it.
