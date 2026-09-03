---
name: ai-landscape
description: Create, review, extend, adopt tools into, or retire an AI landscape of context, skills, workflows, agents, contracts, and enforcement.
metadata:
  version: 3.0.0
---

# Ai Landscape

## Apply When

Use this policy when the work is about the AI landscape itself rather than about the project's own code:

- setting up instructions for an AI tool in a project that has none
- reviewing or trimming an existing instruction system, especially after a model or tool upgrade
- adding or changing one context source, skill, workflow, agent, contract, or enforcement mechanism
- adopting an external tool, plugin, or instruction bundle without importing its demos and scaffolding
- removing a harness the project no longer wants

Do not use it for ordinary work inside a project that already has a landscape. A landscape that only functions when
this policy is loaded has failed its purpose.

## Policy

The framework sources ship with this skill. Resolve every path below against the plugin root, never against the
user's working directory:

- Claude Code substitutes `${CLAUDE_PLUGIN_ROOT}` — read `${CLAUDE_PLUGIN_ROOT}/MANIFEST.md` and
  `${CLAUDE_PLUGIN_ROOT}/IMPLEMENTATION.md`.
- Codex substitutes `$PLUGIN_ROOT` — read `$PLUGIN_ROOT/MANIFEST.md` and `$PLUGIN_ROOT/IMPLEMENTATION.md`.
- If neither variable is substituted, the framework is a plain checkout: search upward from this skill's own directory
  for the directory containing `MANIFEST.md` and use that as the root.

Read `MANIFEST.md` for the values and `IMPLEMENTATION.md` for artifact boundaries before changing anything. The
`workflows/` and `contracts/` directories named below sit beside them under the same root.

Every concern has one home. Facts and preferences belong to context; universal authority limits to the root contract;
task-scoped policies to skills; procedures to workflows; fresh-context responsibilities to agents; data shapes to
contracts; hard guarantees to deterministic enforcement; and reasoning to the model. An artifact must not absorb a
concern that has a better home.

Run the workflow that matches the request rather than improvising a procedure:

| Request | Workflow |
| --- | --- |
| Set up a landscape, or restructure an existing one | `<root>/workflows/setup.yml` |
| Review a landscape for value, conflicts, and stale scaffolding | `<root>/workflows/review.yml` |
| Add or change one bounded capability | `<root>/workflows/extend.yml` |
| Adopt an external tool or instruction bundle | `<root>/workflows/adopt-tool.yml` |
| Remove a harness and keep what was worth keeping | `<root>/workflows/retire.yml` |

Each workflow declares the sources it needs in its own `inputs`. Follow its steps, dependencies, approval gates, and
failure behavior as written; the workflow owns the procedure, not this skill.

## Constraints

- Inspect the repository and any existing landscape before asking questions. Ask only what changes the result.
- Propose before changing files, and record the approved scope as a `change-proposal`.
- Never move, rename, delete, merge, or replace an existing artifact without explicit approval.
- Never commit, push, deploy, publish, or take another external action on your own authority.
- Prefer each selected tool's current native discovery mechanism; verify it against official documentation rather than
  memory.
- Create an artifact only for a present need. An empty layer is worse than a missing one.

## Outcome

The user can describe their work in ordinary language and have the landscape supply the relevant context, policy,
procedure, isolation, contracts, and enforcement quietly. Run `python3 <root>/scripts/validate.py` against the
result; report any check that could not be run.
