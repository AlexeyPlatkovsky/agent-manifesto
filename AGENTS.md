# Maintain Framework Version

Use this skill whenever a task changes the `agent-manifest` framework itself.

This file is not part of the Agent Manifesto framework. Its only purpose is to maintain correct project version bumping.
Do not treat it as a framework source when discussing or designing framework changes. Apply it only when a task requires
a project version bump.

This repository is versioned as a single unit. The following files must always share the same framework version:
- `MANIFEST.md`
- `IMPLEMENTATION.md`
- `README.md`
- `workflows/*.yml`
- `skills/*/SKILL.md`
- `agents/*.md`
- `contracts/*.schema.json`

Markdown sources store the value in YAML frontmatter as `version`. Workflow YAML stores it as the top-level `version`.
JSON Schema contracts store it as `x-framework-version`.

No other file may hardcode the framework version. `MANIFEST.md` is the single source of truth: `scripts/validate-framework.rb`
reads the expected version from it, and `contracts/workflow.schema.json` constrains `version` with a major-version
pattern rather than an exact value. A bump that crosses a major version must widen that pattern.

## Rules

1. Read the version metadata of all files before editing any of them.
2. Keep the framework version identical across all files at all times.
3. When a framework refactor changes the version, update all files in the same patch.
4. Use semantic versioning: `MAJOR.MINOR.PATCH`.

## Semantic Version Policy

- PATCH: wording fixes and clarifications
- MINOR: new skills, new rules, or structural additions
- MAJOR: breaking changes to the framework contract

## Verification

Before declaring the task complete:

1. Run `ruby scripts/validate-framework.rb`.
2. Confirm the framework version values are identical across all files.
3. Confirm the bump level matches the kind of change made.
4. If any file was missed, fix it before reporting completion.

## Commit Messages

Commit messages must describe the project-level change (what was changed, added, patched, fixed, restructured, removed).

Do not frame commits around the version bump itself:
- avoid titles like `Bump version to X`, `Version sync`, `Patch bump for Y`
- prefer titles that describe the substantive change (`Rework README as how-to guide`, `Add README to versioned file
  set`)

The version change is visible in the diff and the release tag — the commit message should explain the change that
justified the bump, not restate the bump.
