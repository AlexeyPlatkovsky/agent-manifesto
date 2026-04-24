---
version: 1.5.4
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/04_tool_integration.md
---

# 04_tool_integration.md — External Tool Adoption

## Context Required

Before starting, ensure the following files are available in this session:
- `MANIFEST.md`
- `protocols/_README.md`
- all canonical protocol files under `protocols/` relevant to the current system
- the current instruction system: root contract, skills, pipelines, agents, and docs
- the external tool being adopted: its repository, documentation, and any skill or pipeline bundle it ships

If required context is missing, stop and ask for it.

---

## Purpose

Adopt an external tool, framework, or library into an existing instruction system without polluting the project with demos, broken artifacts, or a foreign skill system.

This prompt is not for building from scratch and not for general evolution.
It assumes `01_initial.md` already produced a valid baseline, and `03_evolution.md` has been run if the project recently changed scale.

Use it when the user explicitly wants to integrate a specific external tool.

---

## Working Mode

Work in exactly 4 phases:
1. Inventory
2. Reconciliation
3. Composition
4. Cleanup

During Reconciliation, do not write files.
During Composition, do not return to discussion.

---

## Phase 1 — Inventory

Read the external tool as it arrives and the current instruction system.

Identify:
- the tool's runtime surface: libraries, binaries, configuration files actually required to use it
- demo or example content shipped with the tool: sample pages, sample tests, fixtures that must not enter the project
- foreign instruction artifacts shipped with the tool: its own skills, pipelines, agents, or prompt files
- compilation or import integrity: missing imports, broken paths, unresolved types, peer dependencies
- overlap with existing project capabilities: does the tool's skill system duplicate or conflict with yours

Provide a brief inventory summary, then move to Phase 2.
Do not propose solutions yet.

---

## Phase 2 — Reconciliation

Decide how every foreign artifact maps into the project.

For each foreign skill or pipeline the tool ships, choose exactly one disposition:
- translate: create a standalone project skill that captures the tool's mandatory behavior plus minimal project-specific adaptation, then discard the foreign artifact
- wrap: keep the foreign artifact only as a runtime library and expose it through a project skill
- reference: link it as external documentation when the behavior is not needed as a first-class capability
- discard: remove entirely when the project has no real use for it

For demo and example content, the only valid disposition is discard, unless the user explicitly asks to keep specific fixtures.

For broken imports or compilation failures, the only valid disposition is fix or delete.

Present the reconciliation table to the user and ask for approval before Phase 3.

---

## Phase 3 — Composition

Begin only after explicit user approval of the reconciliation table.

Rules:
- follow `MANIFEST.md`
- keep protocol-derived mandatory capabilities intact
- translate foreign skills into standalone project artifacts under the project's existing skill layer
- do not keep the tool's foreign skill bundle inside the project instruction system
- route new capabilities through the existing manager-equivalent when the project has one
- keep execution skills isolated from orchestration
- update the applicable root contract and capability registry with the new skills
- for multi-tool or AI-agnostic projects, emit each translated or generated shared skill as `.ai/skills/<skill_name>/SKILL.md` with Claude-style YAML frontmatter including at least `name` and `description`

For single-tool projects, update the native root entrypoint.
For multi-tool or AI-agnostic projects, update `AGENTS.md` and any selected adapters.

If integration reveals that a protocol-derived mandatory capability is missing for the current project size, stop and require `03_evolution.md` to run first.

---

## Phase 4 — Cleanup

Before declaring integration complete, verify:
- demo pages, demo tests, and vendor sample fixtures are removed
- all imports resolve and the project compiles or type-checks cleanly
- no foreign skill, pipeline, or agent file remains inside the project instruction directories
- the tool's runtime library is the only thing retained from the vendor bundle
- the capability registry and routing layer list every new project skill
- every new non-trivial pipeline ends with `task-complete`

If any check fails, fix it before reporting completion.

---

## Final Summary

After implementation, report:
1. what runtime surface was retained
2. what foreign artifacts were translated, wrapped, referenced, or discarded
3. what new project skills and pipelines were added
4. what was removed during cleanup
5. remaining gaps or follow-ups
6. compliance confirmation
