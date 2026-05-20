---
version: 2.8.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/agents/test-system-kit/builder/SKILL.md
name: test-system-builder
description: Designs and produces a complete drift-test system for a project's AI capabilities — its skills, agents, and pipelines. Project- and tech-agnostic; discovers capability layout and verification commands rather than assuming them. Runs as a skill so it can hold a structured one-decision-at-a-time discussion with the user before producing artifacts.
implementation: optional
requires_when:
  - a project's AI capabilities need a standing drift-test system created or expanded
---

# Test System Builder

## Why This Is A Skill

`test-system-builder` runs as a **skill in the main conversation**, not as an
isolated agent. Its design step is a multi-turn, one-decision-at-a-time
discussion with the user, and that discussion cannot happen inside a subagent
that runs to completion in a single shot. The auditor and the runner are agents;
the builder is deliberately not.

## Purpose

`test-system-builder` builds a drift-test system for the host project's AI
capabilities. It inventories the project's skills, agents, and pipelines, locks
the design through a structured discussion, and produces the complete test
system: directory layout, scenario cards, fixtures, a README, and a runner agent
instantiated from `templates/runner-agent.md`.

The system it produces tests **AI instruction artifacts**, not the product the
project ships. It is a drift check: it confirms each capability still honors its
own contract.

## When To Use

Use `test-system-builder` when a project needs an AI-capability test system
created or substantially expanded. Run it once to bootstrap; run it again later
to extend coverage to new capabilities.

Do not use it to run an existing suite (that is the runner's job) or to audit
one (that is `test-system-auditor`'s job).

## Relationship To `artifact-acceptance-tester`

The framework's `artifact-acceptance-tester` agent and this kit both run
scenario tests against instruction artifacts, but they are not the same tool and
do not replace each other:

- `artifact-acceptance-tester` is a **one-shot acceptance gate** — it runs a
  fixed batch of scenarios against a new or materially changed artifact at the
  moment it is being accepted, and is discarded after.
- `test-system-builder` produces a **standing drift-test suite** — persistent
  scenario cards plus a runner, re-runnable on demand to catch regressions long
  after acceptance.

Use the acceptance tester to gate a change in; use this kit to keep catching
drift afterward. When a project has both, keep their scenario vocabularies
aligned where practical (happy / negative-or-block / misuse-or-edge).

## Tech-Agnostic Principle

This skill makes **no assumption** about the project's language, build tool,
framework, or domain. Anything tech-specific is discovered or asked:

- where capabilities live
- how a capability is invoked
- what verification commands a scenario's implementation step runs
- what command shows uncommitted workspace state

Never hard-code a stack-specific command, path, or tool into produced artifacts.
Every such value flows in through the discovery and discussion steps.

## Procedure

### Step 1 — Discover Capabilities

Inventory the project's AI capabilities before any discussion.

1. Locate the AI-capability root. Check common locations (`.ai/`, `.claude/`,
   `agents/`, `skills/`, `pipelines/`, an `AGENTS.md` or equivalent contract
   file). If the layout is unclear, ask the user.
2. Enumerate every **skill**, **agent**, and **pipeline**. For each, record its
   name, file path, and a one-line summary of its contract — required inputs,
   output contract, refusal/stop behavior, and (for pipelines) stage sequence
   and any loop limits.
3. Note any capability whose contract is too thin to test meaningfully — surface
   it; do not silently skip it.

Produce a capability inventory before Step 2.

### Step 2 — Lock The Design By Discussion

Run a structured discussion to decide the design. If the host project provides a
`brainstorm` skill or equivalent, use it; otherwise conduct the discussion
directly following the same discipline: **one decision per turn, each with 2–3
concrete options and their trade-offs, and stop and wait for the user's choice.**
Never assume a decision was made implicitly.

Decisions to lock (skip any the project has already settled):

- **Capability scope** — which of skills / agents / pipelines to cover; whether
  to exclude capabilities with non-deterministic, hard-to-judge contracts.
- **Test root and layout** — where the suite lives; targets organized as
  `agents/<name>/`, `skills/<name>/`, `pipelines/<name>/`, each with a
  `scenarios/` directory.
- **Card schema** — confirm the schema in `conventions/scenario-card-schema.md`,
  or adapt it. Any adaptation is recorded in the produced README.
- **Fixtures** — shared fixtures directory vs. per-target; what handoff blocks
  need pre-baking.
- **Verification commands** — what a scenario's implementation step runs, and
  the prerequisites for a live run.
- **Results handling** — where the runner writes its log; gitignore policy.
- **Runner naming and placement.**
- **Coverage policy** — the completeness bar (see Step 4).
- **Failure mode** — whether the runner halts on first failure or continues past
  failures. This decision is written into the runner's `{{FAILURE_MODE}}`
  placeholder.

Produce a written decision summary and get the user's confirmation before
Step 3.

### Step 3 — Produce The Test System

Create, per the locked design:

1. **Directory tree** — the test root with a target directory per capability,
   each holding `scenarios/`; a shared fixtures directory; a gitignored results
   directory.
2. **Scenario cards** — for every in-scope capability, against
   `conventions/scenario-card-schema.md` (`templates/scenario-card.md` is the
   fill-in copy). For each capability derive scenarios from its own contract:
   - a **happy-path** scenario exercising the primary success contract;
   - a **negative** scenario per refusal/stop clause (missing or malformed
     required input);
   - an **edge** scenario per non-trivial branch (loop limits, no-context cases,
     boundary conditions);
   - for pipelines, scenarios for stage sequencing, handoff propagation, and
     revision/escalation behavior.
   Every scenario must trace to a specific clause of the capability's contract.
   Number cards per target sequentially from `01` as the schema convention
   defines.
3. **Fixtures** — pre-baked handoff blocks the cards inject in place of running
   an upstream stage.
4. **Runner agent** — instantiate `templates/runner-agent.md`, replacing every
   placeholder (including `{{FAILURE_MODE}}`) with the values from Step 2, and
   write it to the project's agent location.
5. **Test-system README** — purpose, layout, the card schema (and any adaptation
   agreed in Step 2), how to invoke the runner, and a coverage table.
6. **Registry update** — if the project has a capability registry or contract
   file, add the runner to it.

### Step 4 — Coverage Check: No Silent Gaps

Before handoff, build a coverage matrix: every in-scope capability, every clause
of its contract, and the scenario(s) that exercise it. The bar:

- every in-scope capability has at least a happy-path scenario;
- every refusal/stop clause has a negative scenario;
- every non-trivial branch has an edge scenario.

Where a clause is genuinely impractical to test, record it as an **acknowledged
gap** with the reason. An acknowledged gap is acceptable; an unnoticed one is a
defect. State the matrix in the handoff.

### Step 5 — Smoke Run

Prove the produced system actually runs before declaring the build done. Static
production is not evidence the wiring works.

1. Pick one happy-path scenario for one in-scope capability.
2. Invoke the generated runner agent on that scenario's target.
3. Confirm the runner discovers the card, executes it, judges it `PASS`, applies
   cleanup, and leaves the workspace matching its pre-run baseline.

If the smoke run does not produce a clean `PASS` with a restored workspace, the
build is not finished — fix the wiring (card steps, runner placeholders, fixture
paths, verification commands) and smoke-run again. Report the smoke-run outcome
in the handoff.

### Step 6 — Hand Off To The Auditor

Report the produced system, the coverage matrix, and the smoke-run result, and
recommend running `test-system-auditor` to verify the system independently.

## Output Contract

On completion, report:

- the capability inventory
- the locked design decisions
- the produced directory tree and the runner agent path
- the coverage matrix, with any acknowledged gaps called out
- the smoke-run result
- the recommendation to run `test-system-auditor`

## Constraints

`test-system-builder` must NOT:

- hard-code a language-, build-, or framework-specific command, path, or tool
  into any produced artifact
- skip the discovery step, the discussion step, or the smoke run
- produce scenario cards that do not trace to a capability contract clause
- leave a capability uncovered without recording it as an acknowledged gap
- judge or grade its own output — that is `test-system-auditor`'s role
- commit, push, or stage changes
