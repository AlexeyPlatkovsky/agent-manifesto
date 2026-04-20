---
version: 1.4.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/protocols/_README.md
---

# Protocols

This directory contains canonical framework protocols.

Protocols are framework inputs.
They are not copied into projects and are not referenced by project runtime files.

## How To Use Protocols

- Treat each protocol file as the canonical source for that behavior at framework design time.
- Derive capabilities from protocol frontmatter, not from memorized protocol names.
- Use `implementation` and `applies_to` as the authoritative applicability metadata.
- Generate standalone project skills from protocol mandatory rules plus minimal project-specific adaptation.
- Do not make generated project skills depend on `protocols/` files or framework-only paths.

## Current Protocols

### `brainstorm.md`

Structured discussion behavior for open design and architecture decisions.

### `task_complete.md`

Closure reporting for non-trivial work.

### `manager.md`

Centralized routing and completion enforcement for medium and large projects.
