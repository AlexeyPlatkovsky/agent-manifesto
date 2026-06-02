---
version: 2.10.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/protocols/documentation_maintenance.md
implementation: mandatory
requires_when:
  - feature implementation changes project behavior, interfaces, commands, architecture, or domain facts
  - refactoring changes project structure, ownership, public contracts, or documented workflows
  - non-trivial bug fix changes behavior, constraints, commands, or known failure modes
---

# documentation_maintenance.md

## Purpose

This protocol defines canonical documentation maintenance behavior after project changes.

It is a framework input.
Project skills derived from it must be standalone project artifacts.

---

# Related Convention

This protocol applies `conventions/reference-docs.md` as the canonical framework standard for reference doc structure, selective loading, doc roots, and context usage reporting.

Project-local skills derived from this protocol must reference the generated or existing project-local equivalent, not the framework file path, unless the framework convention is intentionally shipped as project-local authority.

---

# Mandatory Implementation Rules

Any project skill derived from this protocol must:
- run after triggered project changes and before final completion reporting
- identify what changed during the task
- determine whether the change affects project documentation
- find the project's authoritative documentation roots before reading or editing docs
- apply the reference-docs standard or its project-local equivalent when creating, updating, reorganizing, or reading reference docs
- update affected docs when the needed documentation change is clear and in scope
- report when documentation does not need changes
- report when documentation should change but cannot be updated safely
- emit a visible output artifact that downstream completion can cite

Projects may adapt the skill to repository-specific doc roots, doc tooling, review requirements, and naming.

---

# When Documentation Maintenance Applies

Documentation maintenance applies after:
- feature implementation that changes project behavior, interfaces, commands, architecture, or domain facts
- refactoring that changes project structure, ownership, public contracts, or documented workflows
- non-trivial bug fixes that change behavior, constraints, commands, or known failure modes

It does not apply:
- to purely exploratory or discussion work
- to trivial edits with no user-visible, developer-visible, operational, or architectural effect
- to documentation-only tasks whose primary execution already updated the relevant docs
- when the project has no meaningful documentation surface to maintain

---

# Core Rules

## 1. Run After The Change

Documentation maintenance is a post-change check.

Do not predict documentation updates before implementation is known.
Inspect the actual diff, changed files, or executed steps before deciding whether docs need maintenance.

## 2. Find Authoritative Doc Roots

Before reading or editing docs, identify the project's authoritative documentation roots from:
- `.ai/docs/project_specification.md`, when present
- the generated root contract or manager-equivalent capability
- existing repository docs and documented conventions
- the project-local reference-docs standard, when present

Do not assume `.ai/docs` is the only valid project documentation location.

## 3. Decide Whether Docs Are Affected

Check whether the change affects:
- public behavior
- user workflows
- developer workflows
- commands, scripts, or environment setup
- architecture, ownership, or source layout
- API, data, or integration contracts
- domain vocabulary or business rules
- known limitations, risks, or failure modes

If none apply, report that no documentation change was needed.

## 4. Update Narrowly

When documentation updates are needed:
- edit only affected docs
- preserve the project's existing documentation style
- keep facts in reference docs and behavior in the correct instruction layer
- update indexes, anchors, or cross-references affected by the change
- avoid broad documentation rewrites unless the task explicitly requires them

If the needed update is unclear, risky, or outside the approved task scope, report the gap instead of guessing.

## 5. Report The Result

The documentation maintenance skill must report one of:
- documentation updated
- documentation checked and no update needed
- documentation update needed but blocked

Blocked reports must name:
- the affected doc area
- why the update could not be made safely
- what decision or source is needed

---

# Output Contract

At the end of the documentation maintenance step, produce a concise documentation maintenance report.

The artifact must begin with the project-local capability name:

`Skill: <documentation-maintenance-capability-name> - output below`

Recommended format:

| Status | Docs Checked | Result |
|--------|--------------|--------|
