---
version: 2.10.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/agents/test-system-kit/conventions/scenario-card-schema.md
---

# scenario-card-schema.md

## Purpose

This convention is the single authority for the scenario card schema used by the
Test System Kit. The builder produces cards against it, the auditor checks cards
against it, and the runner parses cards by it. `templates/scenario-card.md` is a
fill-in copy of this schema, not a second definition — when the two disagree,
this file wins.

## Card Anatomy

A scenario card is one Markdown file under a target's `scenarios/` directory. It
has three parts:

1. a **heading line**;
2. a **metadata preamble** of bold-label lines;
3. a set of `##` **sections**.

## Heading Line

```
# Scenario NN — <Short Name>
```

`NN` is a stable, two-digit, zero-padded identifier. Within a target's
`scenarios/` directory, numbers are assigned sequentially in creation order
starting at `01`. A number is never reused and never renumbered: when a card is
deleted its number is retired, leaving an intentional gap. The next new card in
that directory takes the highest existing number plus one. Numbers therefore
need not be contiguous, but they are unique and stable within a target.

## Metadata Preamble

Three bold-label lines, all required, in this order:

- **Target:** the target directory — `agents/<name>`, `skills/<name>`, or `pipelines/<name>`.
- **Level:** one of `agent`, `skill`, `pipeline`. Must match the target directory: `agent` for `agents/*`, `skill` for `skills/*`, `pipeline` for `pipelines/*`.
- **Fixtures:** fixture file paths injected for this scenario, or `none`.

## Sections

| Section | Required | Notes |
|---|---|---|
| `## Spec` | yes | The input the capability is exercised with — a one- or two-line specification, user story, or task. |
| `## Pipeline notes` | pipeline cards only | The only conditional section. Present on `pipeline`-level cards, omitted on `agent`/`skill` cards. Describes the full stage sequence, revision/loop behavior, and loop limits. |
| `## Steps` | yes | Exact run steps: which capability to invoke, with which prompt/template, which fixtures to inject. Every required input filled explicitly — never relying on inference from surrounding context. The last step evaluates the result against the pass criterion. |
| `## Pass criterion` | yes | The condition that makes the scenario `PASS`, stated concretely enough that a runner can judge `PASS`/`FAIL` without interpretation. Must tie to a specific clause of the capability's contract. |
| `## Cleanup` | yes | How to restore the workspace to its pre-scenario state, when to record `SKIP`, and when to record `FAIL`. `None expected` if the scenario produces no changes. |
| `## Failure signals` | yes | Concrete observable symptoms of a failed run. A diagnostic aid, not a pass gate — but the section itself is mandatory. |

`Pipeline notes` is the only conditional section. Every other section is
required on every card.

## Inline Handoff Blocks

A card may embed an inline handoff block inside a section when a one-off fixture
is not worth promoting to a shared fixture file.

## Registration

The runner discovers cards by globbing `scenarios/*.md`. A card is registered
simply by existing in the right target's `scenarios/` directory — there is no
separate index.

## Adapting The Schema

A host project may adapt this schema during the builder's discussion step. When
it does, the builder records the adapted schema in the produced test-system
README, and the auditor checks cards against that recorded schema rather than
this file. Absent a recorded adaptation, this file is authoritative.
