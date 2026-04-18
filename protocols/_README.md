---
version: 1.2.2
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/protocols/_README.md
---

# Protocols

This directory contains the canonical protocol documents used by the framework.

Protocols define behavioral contracts.
They are reference documents, not executable instructions.

## How To Treat Protocols

- Treat each protocol file as the canonical source for that behavior.
- Prompts and audits should derive mandatory skills from the applicable canonical protocol files, not from a hardcoded list.
- Skills may implement a protocol by reference.
- Skills must not restate a protocol inline unless a project-specific adaptation is truly required.
- `MANIFEST.md` remains the governing framework source of truth.
- This README is an index and summary only. It is not normative policy.

## Protocol List

### `brainstorm.md`

Structured discussion protocol for design, architecture, and workflow decisions.

Use it when:
- a decision is still open
- multiple valid options exist
- trade-offs need to be surfaced before execution

### `task_complete.md`

Closure-reporting protocol for non-trivial work.

Use it when:
- a non-trivial pipeline has finished
- the user needs a clear record of what actually happened
- skipped or changed steps must be made visible

### `manager.md`

Routing and orchestration protocol for medium and large projects.

Use it when:
- a non-trivial task needs centralized routing
- the project has multiple workflows, skills, or agents
- completion enforcement should be applied consistently
