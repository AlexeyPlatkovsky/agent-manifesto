# Maintain Framework Version

Apply these instructions whenever a task changes the `agent-manifest` framework itself.

This file is not part of the Agent Manifesto framework. Its only purpose is to maintain correct project version bumping.
Do not treat it as a framework source when discussing or designing framework changes. Apply it only when a task requires
a project version bump.

This repository is versioned as a single unit. The following files must always share the same framework version:
- `README.md` (repository root)
- `.claude-plugin/marketplace.json` (repository root)
- `plugins/agent-manifesto/MANIFEST.md`
- `plugins/agent-manifesto/IMPLEMENTATION.md`
- `plugins/agent-manifesto/workflows/*.yml`
- `plugins/agent-manifesto/skills/*/SKILL.md`
- `plugins/agent-manifesto/agents/*.md`
- `plugins/agent-manifesto/contracts/*.schema.json`
- `plugins/agent-manifesto/.claude-plugin/plugin.json`
- `plugins/agent-manifesto/.codex-plugin/plugin.json`

`.agents/plugins/marketplace.json` carries no version: Codex takes a plugin's version from its manifest.

Markdown sources store the value in YAML frontmatter as `version`, except `SKILL.md` files, which store it as
`metadata.version` — the Agent Skills spec rejects frontmatter keys it does not define, so a top-level `version` there
breaks packaging. Workflow YAML stores it as the top-level `version`. JSON Schema contracts store it as
`x-framework-version`. Plugin manifests store it as `version`; marketplace catalogs store it as `version` on each
plugin entry.

No other file may hardcode the framework version. `MANIFEST.md` is the single source of truth. Paths below are
relative to `plugins/agent-manifesto/`.

`scripts/validate.py` reads the expected version from `MANIFEST.md`, and `contracts/workflow.schema.json` constrains
`version` with a major-version pattern rather than an exact value. A bump that crosses a major version must widen that
pattern.

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

1. Run `python3 plugins/agent-manifesto/scripts/validate.py`.
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
