---
version: 1.5.1
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/03_evolution.md
---

# 03_evolution.md — Instruction System Evolution

## Context Required

Before starting, ensure the following files are available in this session:
- `MANIFEST.md`
- `protocols/_README.md`
- all canonical protocol files under `protocols/` relevant to the current system
- the current instruction system: root contract, skills, pipelines, agents, and docs

If required context is missing, stop and ask for it.

---

## Purpose

Expand a correct baseline instruction system into a more complete one that reflects real team habits and recurring work.

When the user already asks for specific new capabilities, keep evolution anchored to that explicit request instead of resetting to broad discovery of team habits.

This prompt is not for building from scratch.
It assumes `01_initial.md` already produced a valid baseline.

It is not for adopting external tools, libraries, or frameworks.
If the user's request bundles tool adoption with evolution, split the work: run `03_evolution.md` first, then hand off tool adoption to `04_tool_integration.md`.

---

## Working Mode

Work in exactly 3 phases:
1. Discovery
2. Brainstorm
3. Proposal

During Brainstorm, follow `protocols/brainstorm.md`.
During Proposal, present the full proposal at once.
During Composition, do not return to discussion.

---

## Phase 1 — Discovery

Read the current instruction system and identify:
- what skills, pipelines, agents, and docs already exist
- what recurring work they already cover
- what important recurring work is still missing
- whether the user already named concrete additions or target responsibilities
- which design decisions are still genuinely open versus already decided by the user request
- whether the current system still matches protocol requirements
- whether duplication or blurred responsibilities have crept in

Provide a brief current-state summary, then move to Phase 2.
Do not propose solutions yet.

---

## Phase 2 — Brainstorm

Ask only about unresolved high-impact decisions.

If the user already requested concrete additions, start with a scoped question about that requested capability set.
Do not reset to a broad "typical day or week" discovery prompt.

Use a broad recurring-work question only when the request is intentionally open-ended and the missing capability areas are still unknown.

Every Brainstorm question must follow `protocols/brainstorm.md` exactly:
- one question at a time
- 2-3 concrete options
- explicit trade-offs
- stop and wait after each question

Explore only areas not already covered well by the existing system, such as:
- review habits
- release or deployment routines
- testing and debugging patterns
- onboarding
- docs maintenance
- recurring cross-team coordination
- constraints or variants of the explicitly requested capability set

Do not ask for broad workflow narration when Discovery and the user request already provide enough evidence to discuss the requested additions directly.

Stop when:
- the user has described the meaningful recurring work
- no major new pipelines or specialized roles are emerging
- you have enough evidence to justify a concrete proposal

Before leaving Phase 2, ask whether anything important is still missing.

---

## Phase 3 — Proposal

Present the complete proposed delta all at once.

Group proposals by type:
1. Skills
2. Pipelines
3. Agents
4. Docs

For each proposed addition, provide:
- name
- type
- purpose
- what user-described need justifies it
- what existing artifacts it depends on
- why it belongs in that layer

Before presenting, verify that each proposal:
- does not duplicate an existing artifact
- fits the correct layer
- is justified by actual repository or user evidence

Ask the user to approve, reject, or modify the proposal set before implementation.

---

## Composition

Begin only after explicit user approval.

Rules:
- follow `MANIFEST.md`
- keep protocol-derived mandatory capabilities intact
- if Discovery concluded that project scale changed, materialize every protocol whose `applies_to` now includes the new scale and whose `implementation` is `mandatory` as a standalone project skill before any other addition (for example, a scale bump to `medium` or `large` requires a standalone manager skill derived from `protocols/manager.md`)
- preserve existing good artifacts unless the user approved changes
- keep execution skills isolated from orchestration
- update the applicable root contract and capability registry

For single-tool projects, update the native root entrypoint.
For multi-tool or AI-agnostic projects, update `AGENTS.md` and any selected adapters.
Any new shared skill must use the framework-standard format `.ai/skills/<skill_name>/SKILL.md` with Claude-style YAML frontmatter including at least `name` and `description`.

---

## Final Summary

After implementation, report:
1. what was added
2. what was updated
3. what was intentionally excluded
4. remaining gaps
5. compliance confirmation
