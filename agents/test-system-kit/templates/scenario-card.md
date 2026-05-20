---
version: 2.8.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/agents/test-system-kit/templates/scenario-card.md
---

# Scenario Card Template

This is the fill-in copy of the card schema. The schema itself — field meanings,
which sections are required, the `NN` numbering rule — is defined once in
`conventions/scenario-card-schema.md`. When this template and that convention
disagree, the convention wins.

To author a card: copy everything between the rules below into one Markdown file
under a target's `scenarios/` directory, fill every field, and delete the
guidance in parentheses.

---

# Scenario NN — <Short Name>

**Target:** `<target directory, e.g. agents/<name>, skills/<name>, or pipelines/<name>>`
**Level:** <`agent` | `skill` | `pipeline`>
**Fixtures:** <fixture file paths injected for this scenario, or `none`>

## Spec

> <The input the capability is exercised with — a one- or two-line specification, user story, or task.>

## Pipeline notes

<Pipeline-level cards only — omit this section entirely for agent/skill cards.
Describe the full stage sequence, any revision/loop behavior, and loop limits.>

## Steps

1. <Exact run steps: which capability to invoke, with which prompt/template, which fixtures to inject. Fill every required input explicitly — never rely on inference from surrounding context.>
2. <...>
3. Evaluate the observed result against the pass criterion.

## Pass criterion

<The condition that makes the scenario PASS. State it concretely enough that a runner can judge PASS / FAIL without interpretation. Tie it to a specific clause of the capability's contract.>

## Cleanup

<How to restore the workspace to its pre-scenario state. State when to record SKIP (e.g. a disposable target already exists or is dirty) and when to record FAIL (cleanup cannot restore state without touching unrelated work). Write `None expected` if the scenario produces no changes.>

## Failure signals

<What a failed run looks like — concrete observable symptoms. A diagnostic aid, not a pass gate, but the section is required on every card.>

---

See `conventions/scenario-card-schema.md` for the authoritative schema,
including the `NN` numbering rule and which sections are required.
