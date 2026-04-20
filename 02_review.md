---
version: 1.5.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/02_review.md
---

# 02_review.md — Instruction System Review

## Context Required

Before starting, ensure the following files are available in this session:
- `MANIFEST.md`
- `protocols/_README.md`
- all canonical protocol files under `protocols/` required by this framework version
- the project's full instruction system: root contract, skills, pipelines, agents, and docs

If anything required for review is missing, stop and ask for it.

---

## Purpose

Audit the current instruction system against `MANIFEST.md`.

This is a skeptical review.
Assume the system is wrong until proven correct.

Do not implement fixes before the audit and clarification phases are complete.

---

## Working Mode

Work in exactly 4 phases:
1. Audit
2. Clarification
3. Final Validation
4. Implementation and Verification, only when the user requests it

During Clarification, follow `protocols/brainstorm.md`.
Do not modify files during Phases 1-3.

---

## Phase 1 — Audit

### 0. Root Contract Presence

Determine which root contract model applies.

For single-tool projects:
- verify that the tool's official native entrypoint exists and acts as the full operational contract
- verify the native entrypoint against the tool's current official docs when needed
- verify that supporting artifacts follow the selected tool's native structure

For multi-tool or AI-agnostic projects:
- verify that `AGENTS.md` exists and acts as the root operational contract
- verify that supported tool-specific entry files are thin adapters to `AGENTS.md`
- verify that shared skills use the framework-standard format `.ai/skills/<skill_name>/SKILL.md`
- verify that each shared skill uses Claude-style YAML frontmatter with at least `name` and `description`

In both cases:
- verify that routing and capability declarations are visible from the root contract
- verify that execution details are delegated to skills, pipelines, and agents

### 1. Context Minimization

- is the root contract minimal
- are skills, pipelines, agents, and docs on-demand only
- are tool adapters lightweight

### 2. Separation of Policy and Execution

- does the root contract contain policy rather than execution logic
- are procedures confined to skills and pipelines
- do tool-specific files duplicate project policy

### 3. Progressive Disclosure

- does the system start from direct execution and escalate only when needed
- are pipelines and agents justified by project size and repository evidence

### 4. No Duplication

Check for duplicated rules across:
- root contract and skills
- skills and pipelines
- multiple skills
- docs and skills

### 5. Responsibility Boundaries

- does each file have one responsibility
- do execution skills contain orchestration logic
- do pipelines stay purely orchestration
- does the manager-equivalent stay purely routing and orchestration

### 6. Routing Language Enforcement

Check the main routing gate in the root contract:
- is the language imperative
- is the next concrete capability named
- does the gate appear before capability registry
- is trivial classification explicit
- are validation and completion gates mandatory where required

Descriptive routing remains a critical violation.

### 7. Protocol Inventory and Applicability

- read every canonical protocol under `protocols/`, excluding `protocols/_README.md`
- treat protocol frontmatter as authoritative
- determine the project's confirmed or most likely size
- derive required capabilities from `implementation` and `applies_to`

### 8. Protocol Coverage

For each required protocol, verify:
- a corresponding project capability exists
- the capability is standalone and project-local
- it implements the protocol's mandatory rules
- it includes any needed project-specific adaptation without contradiction

Flag as a major violation if a project skill depends on framework protocol files or framework paths at runtime.

### 9. Imported Capability Adoption

When the project adopted an external framework, starter kit, or reusable capability bundle, verify:
- whether demo residue remains, such as sample pages, sample tests, placeholder fixtures, or example docs that are not justified by the host repository
- whether the imported capability was normalized into the host project's routing model instead of bringing its own competing orchestration
- whether imported skills, pipelines, agents, or registries conflict with the host root contract or duplicate existing project capabilities
- whether the adopted code still compiles or typechecks in the host repository after import
- whether exported files have the required imports and no obvious unresolved references remain
- which concrete validation commands would prove the adoption is intact, even if those commands cannot be run during the review

### 10. Structure and Refactor Risks

Check for:
- near-duplicate capabilities
- monolithic pipeline registries
- mixed AI roots
- stale unsupported tool entrypoints
- oversized files that likely violate single responsibility
- imported orchestration layers that bypass or weaken the project's canonical routing path

### 11. Validation and Completion

- does every non-trivial pipeline include explicit validation
- is `task-complete` enforced for non-trivial work
- are stronger review loops reserved for higher-risk work

---

## Phase 1 Output

Provide:

### Root Contract Report

| Location | Mode | Status | Notes |
|----------|------|--------|-------|
| ... | Single-tool / Multi-tool | Valid / Ambiguous / Missing | ... |

### Protocol Coverage Report

| Protocol | Required for This Project | Expected Capability | Status | Notes |
|----------|---------------------------|---------------------|--------|-------|
| ... | Yes / No | ... | Valid / Missing / Ambiguous / Overbuilt | ... |

### Violations

List findings by severity with file references.
Prioritize:
- critical routing failures
- incorrect root contract model
- duplicated or blurred responsibilities
- protocol coverage failures
- imported-framework adoption failures such as demo residue, broken compilation, or competing orchestration

Then list:
- open ambiguities that require clarification
- residual risks or testing gaps

---

## Phase 2 — Clarification

If genuine ambiguity remains, ask only the minimum questions needed to complete the audit.

Follow `protocols/brainstorm.md` exactly:
- one question at a time
- 2-3 options
- explicit trade-offs
- stop and wait

Do not mix clarification with fixes.

---

## Phase 3 — Final Validation

Produce:
- final verdict: compliant, partially compliant, or non-compliant
- the minimum fix plan required for compliance
- which issues are structural refactors that require user approval

Do not implement until the user explicitly asks.

---

## Phase 4 — Implementation and Verification

Only after user request:
- apply the approved fixes
- verify the resulting system
- report what changed and what remains
