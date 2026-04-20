---
version: 1.5.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/README.md
---

# AI Instruction Framework

The Agent Manifesto is a portable framework designed to organize and streamline AI instruction systems, preventing the "messy" complexity that often arises in growing projects. It operates through a three-stage process: **initial builds** to establish a solid foundation, **system audits** for validation and compliance, and **evolutionary updates** that adapt to a team’s specific habits. T

The framework emphasizes minimalism and logic, recommending that instruction files remain around 150 lines to ensure clarity and performance. It is supporting both single-tool and multi-tool environments. By centralizing core rules and separating execution from orchestration, the manifesto ensures that AI agents remain consistent and manageable over time. Ultimately, this resource provides a structured blueprint for developers to build sustainable, future-proof AI workflows.

---

## What This Repository Contains

- `MANIFEST.md`: the canonical framework contract
- `protocols/_README.md`: protocol index and usage notes
- `protocols/*.md`: canonical protocol definitions used by the prompts
- `01_initial.md`: builds or adjusts a baseline instruction system
- `02_review.md`: audits an instruction system against the framework
- `03_evolution.md`: expands a correct baseline around real team habits
- `04_tool_integration.md`: adopts an external tool or framework into an existing instruction system

---

## Core Model

This framework now supports two root-contract modes:

- Single-tool projects: the selected AI tool's official native entrypoint may hold the full project contract.
- Multi-tool or AI-agnostic projects: `AGENTS.md` is the canonical root contract, and tool-specific files are thin adapters.

For multi-tool shared storage, the default layout is:
- `.ai/skills`
- `.ai/pipelines`
- `.ai/agents`
- `.ai/docs`

Project skills are standalone project artifacts.
They are derived from framework protocols during composition, but they must not reference framework protocol files at runtime.

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

## How To Use The Prompts

### `01_initial.md`

Use this when starting from scratch or when refactoring an existing instruction system.

What it does:
- inventories the repository
- runs a structured discussion for unresolved design choices
- derives required capabilities from protocol metadata
- preserves good existing capability names when they already satisfy the framework
- asks before structural refactors such as splits, moves, merges, or deletions

### `02_review.md`

Use this after significant instruction changes or when you want a compliance audit.

What it does:
- validates the correct root-contract model
- checks routing gates, duplication, and responsibility boundaries
- verifies protocol coverage from structured metadata
- produces a minimal fix plan before any implementation

### `03_evolution.md`

Use this only after a valid baseline exists.

What it does:
- learns real recurring work from the user
- proposes new skills, pipelines, agents, and docs
- keeps additions grounded in actual usage rather than theory
- materializes newly-applicable mandatory protocols as standalone skills when project scale changes

### `04_tool_integration.md`

Use this when adopting a specific external tool, library, or framework into an existing instruction system.

What it does:
- inventories the tool's runtime surface, demos, and foreign instruction artifacts
- reconciles foreign skills into standalone project skills, wrapped libraries, references, or discards
- enforces cleanup of demo content and broken imports before completion

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
- Keep execution skills isolated from orchestration.
- Use `pipeline` terminology consistently.
- Do not duplicate rules across root contracts, skills, pipelines, or docs.
- Do not perform structural refactors silently.

---

## License

© Alexey Platkovsky. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
