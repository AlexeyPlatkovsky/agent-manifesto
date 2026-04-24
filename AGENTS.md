# Maintain Version Frontmatter

Use this skill whenever a task changes the `agent-manifest` framework itself.

This repository is versioned as a single unit. The following files must always share the same `version` value in YAML frontmatter:
- `MANIFEST.md`
- `README.md`
- `01_initial.md`
- `02_review.md`
- `03_evolution.md`
- `04_tool_integration.md`
- `protocols/*.md`

## Rules

1. Read the frontmatter of all files before editing any of them.
2. Keep the `version` field identical across all files at all times.
3. When a framework refactor changes the version, update all files in the same patch.
4. Use semantic versioning: `MAJOR.MINOR.PATCH`.

## Semantic Version Policy

- PATCH: wording fixes and clarifications
- MINOR: new skills, new rules, or structural additions
- MAJOR: breaking changes to the framework contract

## Verification

Before declaring the task complete:

1. Re-read the frontmatter in all files.
2. Confirm the `version` values are identical.
3. Confirm the bump level matches the kind of change made.
4. If any file was missed, fix it before reporting completion.
