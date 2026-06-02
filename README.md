---
version: 2.10.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/README.md
---

# AI Instruction Framework

The Agent Manifesto is a portable, tool-agnostic framework for organizing AI instruction systems. `MANIFEST.md` defines the framework's values and principles; `IMPLEMENTATION.md` defines the practices that apply them. Together they keep instruction systems minimal, explicit, and scalable across single-tool and multi-tool environments.

---

## How To Use

The framework is delivered as a set of stages. A stage is any `NN_name.md` file. Each stage is a self-contained entry point with a declared required context list — attach or reference it in your AI tool and ask the tool to run it. The exact syntax depends on your tool (`@file` in Claude Code, Cursor, and most modern agents), but the idea is the same across all of them:

> `run @<stage-file>.md`

Run `00_project_profile.md` before any other stage. After that, pick the stage that matches your current situation.

---

### Stage 00 — Profile The Project

**When:** before any other framework stage, or when the user's role, duties, tools, or project assumptions changed.

**Run:**
```
run @00_project_profile.md
```

**What happens:**
- The AI captures the project purpose, user role, recurring duties, and AI tool surface.
- It identifies authoritative local sources, domain vocabulary, and quality expectations.
- It optionally researches current best practices when local context is insufficient and the user approves.

**Outcome:** `.ai/docs/project_specification.md`, the reusable profile required by every later stage.

---

### Stage 01 — Compose The Initial System

**When:** starting from scratch, or refactoring an existing messy instruction system.

**Run:**
```
run @01_initial_composition.md
```

**What happens:**
- The AI inventories your repository.
- It reads `.ai/docs/project_specification.md`.
- It asks only unresolved design questions needed for composition.
- It derives required capabilities from protocol metadata.
- It derives required agents from agent template metadata.
- It makes tool-specific adapters explicit enough to enforce the canonical root contract.
- It checks repeated software work such as feature implementation, code review, and code refactoring as pipeline candidates when their steps differ.
- It preserves good existing capability names where they already satisfy the framework.
- It asks before any risky change (splits, moves, merges, deletions, contract choices).

**Outcome:** the smallest coherent instruction system that fully aligns with `MANIFEST.md` and `IMPLEMENTATION.md`.

---

### Stage 02 — Review For Compliance

**When:** after significant instruction changes, or when you want a compliance check on an existing system.

**Run:**
```
run @02_review.md
```

**What happens:**
- Validates the correct root-contract model.
- Checks routing gates, duplication, and responsibility boundaries.
- Verifies protocol coverage from structured metadata.
- Verifies required agent coverage from structured metadata.
- Produces a minimal fix plan before any implementation.

**Outcome:** a compliance verdict and minimum fix plan; fixes are implemented only when explicitly requested.

---

### Stage 03 — Expand Capabilities

**When:** a valid baseline already exists and the team has real recurring workflows to encode.

**Run:**
```
run @03_capability_expansion.md
```

**What happens:**
- Learns recurring work directly from you.
- Proposes new skills, pipelines, agents, conventions, and docs grounded in actual usage.
- Verifies present mandatory protocol triggers and mandatory agent-template triggers before optional additions.

**Outcome:** an instruction system that reflects how your team actually works, without speculative abstractions.

---

### Stage 04 — Adopt External Tools

**When:** adopting a specific external tool, library, or framework into an existing instruction system after a valid baseline exists.

Run Stage 03 first if the tool introduces new capability triggers.

**Run:**
```
run @04_tool_adoption.md
```

**What happens:**
- Inventories the tool's runtime surface, demos, and foreign instruction artifacts.
- Reconciles foreign capabilities into standalone project artifacts, wrapped libraries, references, or discards.
- Enforces cleanup of demo content and broken imports before completion.

**Outcome:** the external tool is cleanly integrated, with no leftover demo noise or conflicting instructions.

---

## What This Repository Contains

- `MANIFEST.md` — framework values and principles
- `IMPLEMENTATION.md` — framework mechanics and operational rules
- `conventions/*.md` — shared framework standards used by multiple framework artifacts
- `protocols/_README.md` — protocol index
- `protocols/*.md` — canonical protocol definitions used by stages
- `agents/*.md` — canonical agent templates copied into generated landscapes when their metadata applies (`agents/_README.md` is the index)
- `00_project_profile.md` — creates or updates the reusable project specification
- `01_initial_composition.md` — builds or adjusts a baseline instruction system
- `02_review.md` — audits an instruction system against the framework
- `03_capability_expansion.md` — expands a correct baseline with new capabilities
- `04_tool_adoption.md` — adopts an external tool or framework into an existing instruction system

---

## License

© Alexey Platkovsky. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
