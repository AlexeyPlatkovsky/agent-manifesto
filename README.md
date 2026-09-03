---
version: 3.0.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/README.md
---

# Agent Manifesto

Agent Manifesto helps you create, review, adjust, or retire a lightweight AI landscape for tools such as Claude Code,
Codex, Gemini CLI, and other capable agents.

It supplies what the model cannot know: your context, preferences, authority boundaries, recurring procedures, and
structured interfaces. It leaves problem-solving and implementation reasoning to the model.

## Landscape Model

- facts and preferences belong to **context**
- universal authority limits belong to the **root contract**
- task-scoped policies belong to **skills**
- procedures belong to **workflows**
- fresh-context responsibilities belong to **agents**
- data shapes belong to **contracts**
- reasoning belongs to the **model**
- hard guarantees belong to **deterministic enforcement**

## Install

Agent Manifesto is packaged as a plugin for both Claude Code and Codex. Installing it gives you the `agent-manifesto`
skill, the universal `brainstorm` and `documentation-maintenance` skills, and — on Claude Code — the
`instruction-evaluator` agent.

**Claude Code**

```text
/plugin marketplace add AlexeyPlatkovsky/agent-manifest
/plugin install agent-manifesto@agent-manifesto
```

**Codex**

```text
codex plugin marketplace add AlexeyPlatkovsky/agent-manifest
codex plugin add agent-manifesto@agent-manifesto
```

Or browse with `/plugins` inside Codex. Start a new session before using it.

Codex plugins have no custom-agent component, so `instruction-evaluator` installs on Claude Code only. On Codex the
framework runs the same independent evaluation in a separate fresh session and says so when it cannot.

You can also skip installation entirely and clone the repository — the workflows work the same way when their files
are simply present.

### Testing a local checkout

Both CLIs accept this repository directly as a marketplace, so a change can be installed and inspected without
publishing anything.

```text
# Claude Code — note the trailing slash; a bare "." is rejected
claude plugin marketplace add ./
claude plugin install agent-manifesto@agent-manifesto --scope local -y
claude plugin details agent-manifesto      # component inventory and token cost

# Codex
codex plugin marketplace add .
codex plugin add agent-manifesto@agent-manifesto
codex plugin list
```

`claude plugin details` is the check that matters: it reports how many skills and agents actually loaded. A component
that fails to load is reported as a count of zero, not as an error, so read the inventory rather than trusting the
install to have succeeded. After editing the repository, run `claude plugin marketplace update agent-manifesto` and
reinstall — the installed copy is a cache, not a link.

Remove the plugins before the marketplaces — removing a marketplace first orphans its plugin cache:

```text
claude plugin uninstall agent-manifesto --scope local
codex plugin remove agent-manifesto@agent-manifesto   # the @marketplace suffix is required

claude plugin marketplace remove agent-manifesto
codex plugin marketplace remove agent-manifesto
```

## Quick Start

Ask for the work in ordinary language and the `agent-manifesto` skill routes to the right workflow. To run one
directly, point your AI tool at it. Each workflow declares the framework sources it needs in its own `inputs`, so you
do not have to attach them by hand.

### Create or adjust a landscape

```text
Run @plugins/agent-manifesto/workflows/setup.yml
```

The setup workflow:

1. inspects the repository and any existing AI landscape
2. infers what it can before asking questions
3. asks only for missing context and meaningful preferences
4. proposes the smallest useful landscape
5. waits for approval before changing files
6. evaluates the result in fresh context

It supports both a new project and an existing landscape.

### Review an existing landscape

```text
Run @plugins/agent-manifesto/workflows/review.yml
```

Use this after significant instruction changes, after a model or tool upgrade, or as a six-month scaffolding reset.

### Add or change a capability

```text
Run @plugins/agent-manifesto/workflows/extend.yml
```

Use this for one bounded addition or change to context, a skill, workflow, agent, contract, or enforcement mechanism.

### Adopt an external tool

```text
Run @plugins/agent-manifesto/workflows/adopt-tool.yml
```

This separates the tool's real runtime value from demos, foreign scaffolding, and conflicting instructions.

### Retire a landscape

```text
Run @plugins/agent-manifesto/workflows/retire.yml
```

Removes a harness you no longer want and keeps what was worth keeping. Durable context, policy, and authority
boundaries move somewhere you choose before anything is deleted. A framework that is maintained by subtraction owes you
a way out.

## What Setup Learns

Only applicable topics are discussed:

- the user's role, business, audience, and recurring work
- project purpose and authoritative sources
- personal versus team-shared scope
- AI tools in actual use
- output and voice preferences
- banned language
- preferred methodologies such as SDD or TDD
- testing and quality expectations
- actions the AI may never take or must ask about

The framework does not ask a software team for a brand voice unless their work requires one.

## Framework Contents

The repository is a marketplace holding one plugin. Everything the plugin ships lives under
`plugins/agent-manifesto/`, so an install copies that directory and nothing else — not the git history, not the CI
configuration.

```text
.claude-plugin/marketplace.json     Claude Code catalog
.agents/plugins/marketplace.json    Codex catalog
plugins/agent-manifesto/
├── .claude-plugin/plugin.json      Claude Code manifest
├── .codex-plugin/plugin.json       Codex manifest
├── MANIFEST.md                     values and principles
├── IMPLEMENTATION.md               artifact boundaries and composition rules
├── workflows/*.yml                 setup, review, extension, adoption, retirement
├── skills/*/SKILL.md               the agent-manifesto entry policy plus task-scoped policies
├── agents/*.md                     fresh-context responsibility templates
├── contracts/*.schema.json         workflow, proposal, and result shapes
├── scripts/validate.py             deterministic check, for this repo or any landscape
└── evals/                          behavioral cases that test whether the framework earns its place
```

`README.md` and `AGENTS.md` stay at the repository root. `AGENTS.md` is not a framework source: it governs version
bumping inside this repository only, and is not copied into a generated landscape.

## Migration From 2.x

Version 3.0 is a breaking simplification:

- numbered Markdown stages become YAML workflows
- pipelines become workflows
- protocol derivation and the generated project-convention layer are removed
- the mandatory manager and task-complete capability are removed
- conversational handoff artifacts are replaced by contracts only where structured data is actually needed
- instruction evaluation remains universal, but scenario-test machinery is no longer generated by default
- the project profile becomes ordinary context created during setup rather than a mandatory preliminary stage
- approved scope becomes a `change-proposal` contract that a script can check against the diff
- retirement becomes a supported workflow instead of an undocumented manual cleanup
- the framework ships as a plugin for the Claude Code and Codex marketplaces

Review existing 2.x landscapes with `plugins/agent-manifesto/workflows/review.yml` before migrating. Moving or
deleting existing artifacts still requires explicit approval.

## Model And Tool Changes

Start model migrations from the smallest prompt that preserves the user's real contract. Retest old instructions rather
than assuming they remain helpful. Durable context stays; model-compensation scaffolding must continue to earn its
place.

## Validate The Framework

```text
python3 plugins/agent-manifesto/scripts/validate.py                 # the framework itself
python3 plugins/agent-manifesto/scripts/validate.py path/to/repo    # a generated landscape
python3 plugins/agent-manifesto/scripts/validate.py --proposal approved-change.json
```

The validator uses only the Python standard library, so it runs inside a generated landscape without installing
anything. It checks workflow shape, skill and agent frontmatter, references between layers, and dependency cycles. Run
against this repository it also checks that every framework source carries the same version.

The setup workflow installs it into the landscapes it creates, so the deterministic check ships with the harness
rather than staying in this repository.

With `--proposal` it also enforces the approved scope: given the change proposal you approved, it reports any file
changed without approval and any private path staged for commit. Approval stops being a promise the model makes and
becomes something you can check.

## Test The Framework Itself

```text
python3 plugins/agent-manifesto/evals/run.py --list
```

Three fixture projects with expectations: a repository that should receive almost no landscape, an over-built 2.x
landscape that should be trimmed without losing its facts, and a healthy landscape the framework must leave alone.
See [plugins/agent-manifesto/evals/README.md](plugins/agent-manifesto/evals/README.md) for the
baseline-comparison method.

## License

© Alexey Platkovsky. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
