---
version: 2.8.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/protocols/_README.md
---

# Protocols

This directory contains canonical framework protocols.

Protocols are framework inputs.
They are not copied into projects and are not referenced by project runtime files.

## How To Use Protocols

This file is an index and must not participate in capability derivation.

Use `conventions/framework-metadata.md` for protocol metadata rules.
Use `conventions/capability-derivation.md` for derivation and generated project capability rules.
Use `conventions/traceability.md` for protocol output contracts that gate downstream work.

## Current Protocols

### `brainstorm.md`

Structured discussion behavior for open design, setup, and profile decisions with meaningful trade-offs.

### `task_complete.md`

Closure reporting for non-trivial routed work.

### `documentation_maintenance.md`

Post-change documentation maintenance after feature implementation, refactoring, and non-trivial bug fixes.

### `manager.md`

Centralized routing and completion enforcement when routing must choose between multiple capabilities.
