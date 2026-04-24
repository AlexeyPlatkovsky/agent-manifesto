---
version: 1.5.4
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/README.md
---

# AI Instruction Framework

The Agent Manifesto is a portable, tool-agnostic framework for organizing AI instruction systems. It prevents the "messy" complexity that grows in AI-assisted projects by centralizing core rules, separating execution from orchestration, and keeping instruction files minimal and logical. It supports both single-tool and multi-tool environments, and scales from small prototypes to large codebases.

---

## How To Use

The framework is delivered as a set of prompt files. Each prompt is self-contained — attach or reference it in your AI tool and ask the tool to run it. The exact syntax depends on your tool (`@file` in Claude Code, Cursor, and most modern agents), but the idea is the same across all of them:

> `run @<prompt-file>.md`

You do not run all prompts in sequence. Pick the one that matches your current situation.

---

### Step 0 — Pick Your Mode

Before running anything, decide which root-contract mode fits your project:

- **Single-tool** — one AI tool is used (e.g., only Claude Code). The tool's native entrypoint holds the full project contract.
- **Multi-tool or AI-agnostic** — multiple AI tools, or you want portability. `AGENTS.md` is the canonical root contract, and tool-specific files are thin adapters.

The prompts will ask you to confirm this, so you do not need to configure anything up front — just know which one you want.

---

### Step 1 — Build The Baseline

**When:** starting from scratch, or refactoring an existing messy instruction system.

**Run:**
```
run @01_initial.md
```

**What happens:**
- The AI inventories your repository.
- It asks you structured questions about project size, tools, and unresolved design choices.
- It derives required capabilities from protocol metadata.
- It preserves good existing capability names where they already satisfy the framework.
- It asks before any risky change (splits, moves, merges, deletions, contract choices).

**Outcome:** the smallest coherent instruction system that fully aligns with `MANIFEST.md`.

---

### Step 2 — Audit For Compliance

**When:** after significant instruction changes, or when you want a compliance check on an existing system.

**Run:**
```
run @02_review.md
```

**What happens:**
- Validates the correct root-contract model.
- Checks routing gates, duplication, and responsibility boundaries.
- Verifies protocol coverage from structured metadata.
- Produces a minimal fix plan before any implementation.

**Outcome:** a validated instruction system and a short, targeted list of fixes if anything is off.

---

### Step 3 — Evolve Around Real Habits

**When:** a valid baseline already exists and the team has real recurring workflows to encode.

**Run:**
```
run @03_evolution.md
```

**What happens:**
- Learns recurring work directly from you.
- Proposes new skills, pipelines, agents, and docs grounded in actual usage.
- Materializes newly-applicable mandatory protocols as standalone skills when project scale changes.

**Outcome:** an instruction system that reflects how your team actually works, without speculative abstractions.

---

### Step 4 — Integrate External Tools

**When:** adopting a specific external tool, library, or framework into an existing instruction system.

**Run:**
```
run @04_tool_integration.md
```

**What happens:**
- Inventories the tool's runtime surface, demos, and foreign instruction artifacts.
- Reconciles foreign skills into standalone project skills, wrapped libraries, references, or discards.
- Enforces cleanup of demo content and broken imports before completion.

**Outcome:** the external tool is cleanly integrated, with no leftover demo noise or conflicting instructions.

---

## What This Repository Contains

- `MANIFEST.md` — the canonical framework contract
- `protocols/_README.md` — protocol index and usage notes
- `protocols/*.md` — canonical protocol definitions used by the prompts
- `01_initial.md` — builds or adjusts a baseline instruction system
- `02_review.md` — audits an instruction system against the framework
- `03_evolution.md` — expands a correct baseline around real team habits
- `04_tool_integration.md` — adopts an external tool or framework into an existing instruction system

---

## Core Model

This framework supports two root-contract modes:

- **Single-tool projects:** the selected AI tool's official native entrypoint may hold the full project contract.
- **Multi-tool or AI-agnostic projects:** `AGENTS.md` is the canonical root contract, and tool-specific files are thin adapters.

For multi-tool shared storage, the default layout is:
- `.ai/skills`
- `.ai/pipelines`
- `.ai/agents`
- `.ai/docs`

Project skills are standalone project artifacts. They are derived from framework protocols during composition, but they must not reference framework protocol files at runtime.

In multi-tool or AI-agnostic projects, the framework-standard skill format is:
- `.ai/skills/<skill_name>/SKILL.md`
- Claude-style YAML frontmatter with at least `name` and `description`

Single-tool projects should still use the selected tool's native supporting-artifact structure.

---

## Protocol Metadata

Protocol frontmatter is authoritative for derivation and review.

Each protocol declares:
- `implementation: mandatory | optional`
- `applies_to: [small, medium, large]`

In the bundled protocol set:
- `brainstorm` is mandatory for all project sizes
- `task-complete` is mandatory for all project sizes
- `manager` is mandatory for medium and large projects

---

## Typical Outcomes

### Small Project
- minimal root contract
- mandatory protocol-derived skills
- no reference docs by default
- no manager by default
- no agents by default

### Medium Project
- manager-equivalent routing capability
- at least one pipeline
- reference docs: `architecture.md`, `conventions.md`, `commands.md`
- explicit validation on every non-trivial pipeline

### Large Project
- manager-equivalent routing capability
- multiple pipelines as needed
- reference docs: `architecture.md`, `conventions.md`, `commands.md`
- selective agents when context isolation is clearly justified

---

## Operating Rules

- Keep instruction files near 150 lines when possible without harming quality.
- Prefer minimal, surgical changes that trace directly to the user's request.
- Keep execution skills isolated from orchestration.
- Use `pipeline` terminology consistently.
- Do not duplicate rules across root contracts, skills, pipelines, or docs.
- Do not perform risky changes silently.

---

## License

© Alexey Platkovsky. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
