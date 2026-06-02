---
version: 2.10.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/conventions/framework-metadata.md
---

# framework-metadata.md

## Purpose

This convention defines metadata standards for framework source files.

## Shared Frontmatter

Every framework source with YAML frontmatter must declare:
- `version`
- `project`
- `url`

## Protocol Frontmatter

Every canonical protocol under `protocols/`, excluding `protocols/_README.md`, must also declare:
- `implementation: mandatory | optional`
- `requires_when: [...]`

Protocol `requires_when` entries are human-readable trigger phrases. Write them with spaces rather than slug-style underscores.

## Agent Template Frontmatter

Every canonical agent template under `agents/`, excluding `agents/_README.md`, must also declare:
- `name`
- `description`
- `implementation: mandatory | optional`
- `requires_when: [...]`

Agent template `requires_when` entries follow the same wording standard as protocol triggers.

## Metadata Authority

Protocol and agent template frontmatter is authoritative for derivation and review.

Prompt logic must not infer applicability from prose when metadata is present.

