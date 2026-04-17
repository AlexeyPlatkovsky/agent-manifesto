# 03_evolution.md — Instruction System Evolution

## Context Required

Before starting, ensure the following files are available in this session:
- `MANIFEST.md` — canonical source of truth
- `brainstorm_protocol.md` — canonical brainstorming behavior
- Your current instruction system: `AGENTS.md`, all skills, workflows, and agents

If any are missing, stop and ask the user to provide them.

---

## Purpose

Your task is to expand the project's AI instruction system from a minimal viable set into a **comprehensive system** that reflects how the team actually works.

This prompt is NOT for building from scratch.
It assumes `01_initial.md` has already been completed and a baseline instruction system exists.

The goal: discover real workflows, daily routines, and team habits — then translate them into skills, agents, and workflows that genuinely help.

---

## Working Mode

Work in exactly 3 phases. Do not skip or merge phases.

1. **Discovery** — read existing instructions, understand the current state
2. **Brainstorm** — free-form conversation to surface real workflows
3. **Proposal** — present a complete set of proposed additions for user approval

During Brainstorm: follow `brainstorm_protocol.md` exactly.
During Proposal: present everything at once, do not drip-feed proposals.
During Composition (after approval): execute without returning to discussion.

---

## Phase 1 — Discovery

Read and analyze all existing instruction files provided in this session.

Identify:
- what skills, workflows, and agents already exist
- what tasks they cover
- what is NOT yet covered
- obvious gaps between current instructions and a mature project of this type

Also note:
- any MANIFEST violations introduced since initial setup
- any duplication that crept in
- any skills that have grown beyond a single responsibility

### Phase 1 Output

Provide a brief current-state summary:
- what the instruction system covers today
- visible gaps
- any compliance issues to flag

Then transition immediately to Phase 2.
Do NOT propose solutions yet.

---

## Phase 2 — Brainstorm

This is the core phase. Its goal is to extract real workflow knowledge from the user through open conversation.

### Starting Point

Begin with an open invitation — not a structured interview:

> "To build an instruction system that reflects how you actually work, I'd like to understand your team's daily routines and workflows. Describe a typical day or week — what tasks come up repeatedly, what slows you down, what you wish the AI could handle better."

Let the user respond freely. Do not impose structure yet.

### Follow-up Questioning

After the user's initial response, use `brainstorm_protocol.md` to ask targeted follow-up questions:
- one question at a time
- focus on areas not yet covered by existing instructions
- explore: code review habits, deployment routines, testing workflows, onboarding, documentation, debugging patterns, release processes, cross-team communication

Continue until you have sufficient understanding to propose meaningful additions.

### Clustering

As the conversation progresses, mentally cluster what you hear into candidate categories:
- **Skills** — atomic, repeatable tasks
- **Workflows** — multi-step processes with a defined order
- **Agents** — roles that benefit from context isolation
- **Reference docs** — reusable knowledge referenced by multiple skills

Do not share this clustering with the user during the brainstorm phase.
It informs the proposal in Phase 3.

### When to Stop

Stop brainstorming when:
- the user has described their full routine
- no significant new workflows are emerging from follow-up questions
- you have enough to make a meaningful, justified proposal

Ask the user explicitly: "Is there anything else about your workflows or pain points before I propose additions?"

---

## Phase 3 — Proposal

Present the complete proposed delta **all at once**.

Do not drip-feed one proposal at a time.
The user reviews the full picture before anything is created.

### Proposal Format

For each proposed addition, provide:

**[Type: Skill / Workflow / Agent / Reference Doc]**
**Name:** `name`
**Purpose:** one sentence
**Justified by:** what the user described that motivates this
**Depends on:** any existing skills or docs it references
**MANIFEST compliance note:** confirm it follows the correct layer rules

Group proposals by type:
1. Skills (list all)
2. Workflows (list all, only if justified)
3. Agents (list all, only if justified)
4. Reference docs (list all, only if reused by multiple skills)

### Compliance Check

Before presenting, verify each proposal against `MANIFEST.md`:
- does it duplicate anything that already exists?
- does it belong in the correct layer?
- is it truly atomic (for skills)?
- is it only orchestration (for workflows)?
- is context isolation genuinely needed (for agents)?

Remove or reshape any proposal that fails this check.

### After Presenting

Ask the user:
- to approve, reject, or modify individual proposals
- whether priority ordering is needed
- whether anything is missing

Do NOT begin creating files until the user explicitly approves.

---

## Composition

Only begin after explicit user approval of the proposal.

### Rules

- Follow all `MANIFEST.md` principles
- Do not introduce duplication
- Maintain clean responsibility boundaries
- Update `AGENTS.md` to register all new capabilities
- Brainstorm skill must remain present and unchanged unless the user explicitly requests modification

### Output

For each approved addition, create the appropriate file.
After all files are created, provide:

### Final Summary

1. **What was added** — list of all new files and their purpose
2. **What was updated** — any existing files modified (e.g., AGENTS.md)
3. **What was intentionally excluded** — proposals rejected and why
4. **Remaining gaps** — anything identified but deferred for a future evolution session
5. **Compliance confirmation** — brief statement that the updated system follows MANIFEST

---

## Quality Bar

The evolved system must:
- be grounded in real workflows, not theoretical ideals
- introduce no duplication
- stay within correct architectural layers
- be fully registered in `AGENTS.md`
- remain comprehensible — complexity must be justified, not assumed
- retain the brainstorm skill unchanged

If a proposed addition cannot be clearly justified by something the user described → do not add it.
