---
version: 2.10.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/conventions/skill-vs-agent.md
---

# skill-vs-agent.md

## Purpose

This convention defines how to classify an execution capability as a skill or an agent. It is the shared standard the stages and `conventions/layer-purity.md` reference whenever an execution capability is created or audited.

`IMPLEMENTATION.md` §Skills and §Agents define the two layers. This convention does not restate those definitions; it owns the test that decides which layer a capability belongs to.

The discriminator is context locality, as defined for each layer in `IMPLEMENTATION.md` §Skills and §Agents. The decision is binding, not stylistic.

## Decision Test

State the decision and its justification out loud whenever an execution capability is created or audited:
- choose a **skill** when the work needs the main agent's live context, must interact with the user mid-task, or must produce output that the next step uses inline
- choose an **agent** when the work has a clearly defined input and output and runs to completion in an isolated context without live user interaction

Isolation — and therefore an agent — is justified by:
- protecting the main context from large or noisy work
- an independent, unbiased pass such as review, audit, or test
- parallelizable independent work

## Hard Constraints

- work that requires multi-turn user interaction cannot be an agent
- work that requires a clean isolated context returning a result cannot be a skill
- specialized reasoning alone does not make something an agent; a skill may reason. Isolation is the test.

## Failure Signals

Flag misclassification when:
- an agent is used for work that requires multi-turn user interaction
- a skill is used for work that requires an isolated context or an independent unbiased pass
- skill and agent are treated as interchangeable for the same responsibility

Layer-internal boundary violations — a skill body that sequences siblings, an agent body that duplicates root policy — are owned by `conventions/layer-purity.md`.
