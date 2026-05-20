---
version: 2.8.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/04_tool_adoption.md
---

# 04_tool_adoption.md — External Tool Adoption

## Context Required

Before starting, ensure the following files are available in this session:
- `MANIFEST.md`
- `IMPLEMENTATION.md`
- all framework convention files under `conventions/`
- `protocols/_README.md`
- frontmatter for all canonical protocol files under `protocols/`, excluding `protocols/_README.md`; full bodies only for triggered protocols
- frontmatter for all canonical agent template files under `agents/`, excluding `agents/_README.md`; full bodies only for triggered templates
- `.ai/docs/project_specification.md`
- the current instruction system: root contract, skills, pipelines, agents, conventions, and docs
- the external tool being adopted: its repository, documentation, and any instruction bundle it ships

If `.ai/docs/project_specification.md` is missing, stop and require `00_project_profile.md` first.

If other required context is missing, stop and ask for it.

Use `protocols/_README.md` only as an inventory index. Derive capabilities using `conventions/capability-derivation.md`.

---

## Purpose

Adopt an external tool, framework, or library into an existing instruction system without polluting the project with demos, broken artifacts, or a foreign skill system.

Use `.ai/docs/project_specification.md` to decide whether the tool's capabilities are relevant to the user's role, recurring duties, quality expectations, and project context.

This stage is not for building from scratch and not for general capability expansion.
It assumes `01_initial_composition.md` already produced a valid baseline, and `03_capability_expansion.md` has been run if the tool introduces new capability triggers.

Use it when the user explicitly wants to integrate a specific external tool.

---

## Working Mode

Work in exactly 4 phases:
1. Inventory
2. Reconciliation
3. Composition
4. Cleanup

During Reconciliation, do not write files.
During Composition, do not return to reconciliation or discussion. Pause only for explicit approval or clarification gates required by `IMPLEMENTATION.md`.

---

## Phase 1 — Inventory

Read the external tool as provided and the current instruction system.

Identify:
- the tool's runtime surface: libraries, binaries, configuration files actually required to use it
- demo or example content shipped with the tool: sample pages, sample tests, fixtures that must not enter the project
- foreign instruction artifacts shipped with the tool: its own skills, pipelines, agents, conventions, rules, contracts, or prompt files
- compilation or import integrity: missing imports, broken paths, unresolved types, peer dependencies
- overlap with existing project capabilities: does the tool's skill system duplicate or conflict with yours
- whether the tool introduces mandatory protocol or agent-template triggers that require `03_capability_expansion.md` before adoption continues

Provide a brief inventory summary, then move to Phase 2.
Do not propose solutions yet.

---

## Phase 2 — Reconciliation

Decide how every foreign artifact maps into the project.

For each foreign skill, pipeline, or agent the tool ships, choose exactly one disposition:
- translate: create a standalone project capability in the correct layer with the tool's mandatory behavior plus minimal project-specific adaptation, then discard the foreign artifact
- reference: link it as external documentation when the behavior is not needed as a first-class capability
- discard: remove entirely when the project has no real use for it

For executable tool code or APIs, choose exactly one disposition:
- wrap: keep executable tool code or APIs only as part of the approved runtime surface and expose them through a project skill or pipeline
- reference: link it as external documentation when direct project integration is not needed
- discard: remove entirely when the project has no real use for it

For each foreign convention, rule, contract, or prompt file, choose exactly one disposition:
- translate: create a project convention when at least two skills or agents need the same retained behavior
- reference: link it as external documentation when it is useful context but not binding project behavior
- discard: remove it when it is unused, duplicative, demo-only, or conflicts with the host instruction system

For demo and example content, the only valid disposition is discard, unless the user explicitly asks to keep specific fixtures.

For broken imports or compilation failures, the only valid disposition is fix or delete.

If adoption introduces unresolved mandatory capability or framework agent triggers, stop here and require `03_capability_expansion.md` before Phase 3 approval.

Present the reconciliation table to the user and ask for approval before Phase 3.

The reconciliation table must include:

| Artifact | Type | Disposition | Reason | Project target | Risk / approval needed |
| --- | --- | --- | --- | --- | --- |

---

## Phase 3 — Composition

Begin only after explicit user approval of the reconciliation table.

Apply `IMPLEMENTATION.md` §Stage Standards §Composition Anchor.

Stage-specific rules:
- translate retained foreign capabilities into standalone project artifacts under the correct project layer
- do not keep the tool's foreign instruction bundle inside the project instruction system
- route new capabilities through the existing manager-equivalent when the project has one
- apply `conventions/traceability.md` to every translated capability that gates downstream non-trivial routed work
- update the applicable root contract and capability registry with each new capability
- after creating or updating project-local instruction artifacts, verify the project-local instruction-evaluator agent exists, then use it to review those artifacts before final acceptance
- verify the project-local artifact-acceptance-tester agent exists when its trigger applies, then use it to run 9 scenario tests for each new or materially changed runtime instruction artifact before final acceptance

---

## Phase 4 — Cleanup

Before declaring integration complete, verify:
- demo pages, demo tests, and vendor sample fixtures are removed
- all imports resolve and the project compiles or type-checks cleanly
- no foreign skill, pipeline, agent, convention, rule, contract, or prompt file remains inside the project instruction directories
- the approved runtime surface is the only thing retained from the vendor bundle
- the root contract's capability registry lists every new project capability
- every required framework agent is present as a project-local on-demand agent
- the root contract or manager-equivalent enforces `task-complete` for non-trivial routed work

Phase 4 is verification-only unless the required fix is already covered by prior Phase 3 approval. If any check fails and the fix is not covered by prior approval, stop, name the failure and risk, and ask for approval for a new composition/fix pass.

---

## Final Summary

After implementation, report:
1. what approved runtime surface was retained
2. what foreign artifacts were translated, wrapped, referenced, or discarded
3. what new project capabilities were added
4. what was removed during cleanup
5. remaining gaps or follow-ups
6. compliance confirmation
