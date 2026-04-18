---
version: 1.2.1
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/01_initial.md
---

# 01_initial.md — Initial Instruction Composition

## Context Required

Before starting, ensure the following files are available in this session:
- `MANIFEST.md` — canonical source of truth
- `protocols/brainstorm.md` — canonical brainstorming behavior
- `protocols/task_complete.md` — canonical task completion behavior
- `protocols/manager.md` — canonical manager behavior for medium and large projects

If any are missing, stop and ask the user to provide them.

---

## Purpose

Your task is to create a minimal, correct AI instruction system for this project — or adjust the existing one — so it fully aligns with `MANIFEST.md`.

You must also:
- ask the user two mandatory questions during Discussion: intended project size and which AI tools are in use
- ensure every AI tool entry point routes to `AGENTS.md`
- derive mandatory skills from the applicable protocols

The goal is the **smallest coherent system that fits the project today**.
Do not design for a future that does not yet exist.
Do not add complexity that the project does not justify.

---

## Working Mode

Work in exactly 3 phases. Do not skip or merge phases.

1. **Inventory** — understand the project
2. **Discussion** — resolve key decisions with the user
3. **Composition** — create or adjust the instruction system

During Discussion: follow `protocols/brainstorm.md` exactly.
During Composition: do not return to discussion.

---

## Phase 1 — Inventory

Investigate the repository thoroughly before forming any opinions.

### A. Project Nature
- What kind of project is this?
- Likely scale: small / medium / large
- Maturity: prototype / active development / stable / legacy
- Single-purpose or multi-domain?

### B. Tech Stack
- Languages, frameworks, test stack
- Build tools, CI/CD
- Deployment or runtime environment

### C. Existing Documentation
- Root docs, design docs, architecture docs
- Conventions, workflow docs
- Any existing AI instruction files
- Any duplicated or conflicting guidance

### D. Existing Instruction System
- Does `AGENTS.md` exist?
- Do skills / workflows / agents already exist?
- Does routing logic exist?
- Does the current setup violate `MANIFEST.md`?

### E. AI Tool Surface
- Which AI tools are already configured or obviously intended? (Claude Code, Cursor, Codex, etc.)
- Do tool-specific files exist?
- Do those files defer to `AGENTS.md` or duplicate policy?

### F. Reusable Project Knowledge
Identify whether the project needs reference docs such as:
- architecture overview
- code conventions
- test conventions
- domain rules
- repo structure / commands

Do not decide what to create yet. Only identify likely needs.

---

## Phase 1 Output

Stop after inventory and provide:

1. **Project summary** — nature, scale, maturity
2. **Current instruction system summary** — what exists, what is missing
3. **Initial compliance check** — obvious MANIFEST violations in current setup
4. **Main risks / gaps / ambiguities** — what needs clarification before proceeding
5. **Proposed discussion agenda** — the decisions that must be resolved

Do NOT start editing or creating files yet.
Do NOT propose solutions yet.

---

## Phase 2 — Discussion

Resolve the decisions identified in Phase 1 with the user.

Follow `protocols/brainstorm.md` for all discussion behavior:
- one question at a time
- 2–3 concrete options per question
- highlight trade-offs and risks
- stop and wait after each question
- never mix discussion with execution

The first two questions are mandatory, even if the repository suggests an answer:
1. confirm the intended project size (`small`, `medium`, or `large`)
2. identify which AI tools are in use now or must be supported immediately

Ask them one at a time, following `protocols/brainstorm.md`.

Focus discussion on high-impact decisions only:
- appropriate project scale assumption
- how each AI tool should be wired to `AGENTS.md`
- whether workflows are justified
- whether subagents are justified
- which reference docs are worth creating
- how strict validation should be
- whether existing docs should be refactored or preserved

Do not ask about things already clearly established by the repository.
Do not ask trivial questions.

At the end of discussion, produce a **decision summary** and ask the user to confirm before proceeding.

---

## Phase 3 — Composition

Only begin after the user confirms the decision summary.

### Design Rules

- `MANIFEST.md` is the canonical source — never contradict it
- `AGENTS.md` is the project-level operational contract
- all tool-specific adapters must defer to `AGENTS.md`
- Policy and execution must be separated
- Root instructions must stay compact
- Detailed procedures must be modular
- No duplicated logic across files
- Complexity must be progressively disclosed
- The system must match the actual project scale
- mandatory skills must be derived from the applicable protocols

### Required: Mandatory Gate Language in AGENTS.md

Per `MANIFEST.md` Principle 9, routing rules must be written as imperative blocking instructions — not classification tables or descriptive guidance.

**Non-compliant (never produce this):**
```
Non-trivial tasks should be routed via the manager skill.
```
```
| Non-trivial + Low Risk | Workflow + validation |
```

**Compliant (always produce this pattern):**
```
## Task Routing — MANDATORY

Before taking any action, classify the task:

**If the task is trivial (isolated, low-risk, no orchestration needed):**
Proceed directly. State your classification explicitly.

**If the task is non-trivial:**
STOP. Do not write any code, create any files, or begin implementation.
Load [exact routing skill or agent name] NOW.
Do not proceed until routing is resolved.

**If unsure:**
Treat as non-trivial. STOP and load the project's default routing capability.
```

Apply this pattern to:
- the main routing gate at the top of AGENTS.md
- any required completion steps (validation, review loops)
- any skills declared as mandatory for a task type

The gate MUST appear **before** the capability registry in AGENTS.md.
It is the first thing the AI reads.
Do NOT leave placeholders like `[exact routing skill or agent name]` in the final output.
Replace them with the concrete capability the generated system requires.

---

### Required: Brainstorm Skill
This is mandatory per `MANIFEST.md`.

Create `.claude/skills/brainstorm/SKILL.md` that:
- references `protocols/brainstorm.md` as its behavior source
- does not redefine the protocol inline
- is registered in `AGENTS.md`

### Required: Task-Complete Skill
This is mandatory per `MANIFEST.md`.

Create `.claude/skills/task-complete/SKILL.md` in the project's skills directory.

The task-complete skill must:
- reference `protocols/task_complete.md` as its behavior source
- not redefine the protocol inline
- be registered in `AGENTS.md` under the capability registry

Wire it into the manager skill: the manager must append `task-complete` as the final step for all non-trivial pipelines at routing time.
Do not make individual pipelines declare `task-complete` themselves.

### Required: Manager Skill for Medium and Large Projects

If the project is medium or large, create `.claude/skills/manager/SKILL.md`.

The manager skill must:
- reference `protocols/manager.md` as its behavior source
- centralize non-trivial routing
- append `task-complete` as the final step for every non-trivial pipeline
- avoid duplicating `AGENTS.md`
- avoid embedding implementation steps

For small projects, prefer minimal inline routing in `AGENTS.md` unless repository evidence clearly justifies a manager.

### Composition Steps

1. Decide which instruction artifacts are actually needed
2. Map applicable protocols to mandatory skills for the chosen project size
3. Propose the minimal coherent target structure
4. Create or refactor the files
5. Create or refresh tool-specific adapter files so every supported AI tool points to `AGENTS.md`
6. Remove or merge duplicated logic
7. Keep responsibility boundaries explicit

### Output by Project Size

Follow the project size guidelines defined in `MANIFEST.md` (`# Project Size Guidelines`).
Do not force a large-project architecture onto a small repo.

---

## Final Output Format

When composition is complete, provide:

### 1. Final Assessment
- what was found
- what was wrong or missing
- what decisions were made

### 2. Target Architecture
- what files now exist or were created
- what each file is responsible for

### 3. Change Summary
- what was created
- what was updated
- what was removed or merged

### 4. Remaining Trade-offs
- what is intentionally kept simple
- what can be added later if the project grows

---

## Quality Bar

The final system must:
- align with `MANIFEST.md` fully
- be project-specific, not generic filler
- be as small as possible, but complete
- avoid unnecessary abstraction
- avoid duplicated rules
- be understandable from `AGENTS.md` alone

If the project does not justify complexity → explicitly keep it simple.
