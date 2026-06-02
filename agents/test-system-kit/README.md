---
version: 2.10.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/agents/test-system-kit/README.md
---

# Test System Kit

A project- and tech-agnostic framework input for building a **drift-test
system** for a project's AI capabilities — its skills, agents, and pipelines.

## What It Tests

This kit builds a system that tests **AI instruction artifacts** (skills,
agents, pipelines), not the product the project ships. Because instruction
artifacts are Markdown contracts regardless of the project's tech stack, the kit
is tech-agnostic: it works the same for a web project, a mobile project, a CLI
tool, or anything else.

Anything tech-specific — what verification commands a scenario runs, where
capabilities live, how a capability is invoked — is **discovered or asked**,
never assumed. No language, build tool, or framework is hard-coded anywhere in
this kit.

## Relationship To `artifact-acceptance-tester`

The framework's [`artifact-acceptance-tester`](../artifact-acceptance-tester.md)
agent also runs scenario tests against instruction artifacts, but the two serve
different moments and do not replace each other:

- `artifact-acceptance-tester` — a **one-shot acceptance gate**: a fixed batch of
  scenarios run against a new or materially changed artifact at acceptance time.
- this kit — a **standing drift-test suite**: persistent scenario cards plus a
  runner, re-runnable on demand to catch regressions long after acceptance.

Use the acceptance tester to gate a change in; use this kit to keep catching
drift afterward.

## Contents

| File | Role |
|---|---|
| `builder/SKILL.md` | `test-system-builder` — a **skill** that designs and produces a complete test system for the host project |
| `auditor/AGENT.md` | `test-system-auditor` — an **agent** that reviews a produced test system for coverage gaps and contract soundness |
| `conventions/scenario-card-schema.md` | The authoritative scenario card schema |
| `templates/runner-agent.md` | Template the builder instantiates into the host project's scenario runner agent |
| `templates/scenario-card.md` | Fill-in copy of the card schema |

The builder is a **skill**, not an agent: its design step is a multi-turn,
one-decision-at-a-time discussion with the user, which a single-shot subagent
cannot hold. The auditor is an agent (autonomous, read-only). The runner is
**generated** per project from `templates/runner-agent.md` — it ships as a
template, not a pre-built agent, because it must carry that project's capability
layout and verification commands.

## How To Apply (Derive, Don't Copy)

This kit is a **framework input**, applied through the framework's normal
derivation model — see [`conventions/capability-derivation.md`](../../conventions/capability-derivation.md).
It is not copy-pasted into target projects.

1. In the target project's instruction system, **derive** `test-system-builder`
   as a project-local skill and `test-system-auditor` as a project-local agent,
   preserving each artifact's role, constraints, and output contract, and
   adapting only references that the target landscape does not ship.
2. Invoke the derived `test-system-builder`. It discovers the project's
   capabilities, runs its design discussion, produces the suite, and generates
   the runner from `templates/runner-agent.md`.
3. When the builder finishes, invoke `test-system-auditor` to verify the result.

The kit adapts to each target project through the builder's discovery and
discussion steps — nothing in the kit itself needs editing per project.

## Workflow

```
test-system-builder  (skill — runs in the main conversation)
  ├─ discovers the project's skills / agents / pipelines
  ├─ runs a structured one-decision-at-a-time discussion to lock the design
  ├─ produces: directory tree, scenario cards, fixtures, README,
  │            and the runner agent (from templates/runner-agent.md)
  ├─ smoke-runs one happy-path scenario to prove the system runs
  └─ hands off to ↓

test-system-auditor  (agent — autonomous, read-only)
  ├─ re-inventories the project's capabilities
  ├─ checks every capability + every contract clause for scenario coverage
  ├─ checks card-schema conformance and runner-contract soundness
  └─ reports a coverage matrix + gap findings + verdict
```

The builder produces; the auditor judges. They are kept separate so the builder
never grades its own work.

## Design Principle: No Silent Gaps

The builder must achieve coverage that leaves **no silent gaps**. Every
capability gets at least baseline scenarios, and every scenario traces to a
clause of the capability's own contract. Where coverage is genuinely
impractical, the builder must surface that explicitly — an acknowledged gap is
acceptable; an unnoticed one is not. The builder also smoke-runs the produced
system before handoff, and the auditor exists to catch any gap the builder
missed.
