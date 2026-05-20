---
version: 2.8.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/MANIFEST.md
---

# MANIFEST.md

## Purpose

This document defines what the agent-manifest framework values and what must be true of a well-designed AI instruction system.

It does not define file layouts, derivation rules, or runtime mechanics. For how these principles are applied in practice, see [IMPLEMENTATION.md](IMPLEMENTATION.md).

---

# Values

The framework values:

- useful context over complete context
- clear authority over convenient duplication
- direct execution over premature orchestration
- explicit decisions over inferred behavior
- current need over speculative design
- user consent over autonomous risky change

The items on the right still matter, but the items on the left matter more.

---

# Principles

Six principles, two per group. Each is meant to be remembered as a short phrase you can apply without rereading.

## Context And Simplicity

### 1. Load Only What You Need

Default context should contain only what the current work needs to begin correctly.

**Prefer:**
- Small always-available instructions
- Capabilities loaded when relevant
- Clear entry points into deeper guidance

**Avoid:**
- Carrying task-specific guidance everywhere
- Adding context as a substitute for design
- Treating more instruction as automatically safer

---

### 2. Earn Complexity

The smallest structure that solves the real current problem wins. Layers, abstractions, and coordination must be justified by real risk, repetition, or scale — not by imagined futures.

**Prefer:**
- Direct handling for simple work
- Generalization after the pattern is proven
- Changes traceable to an actual requirement

**Avoid:**
- Speculative configurability and single-use abstractions
- Starting with the heaviest structure available
- Treating complexity as evidence of quality

---

## Authority And Structure

### 3. One Artifact, One Job

Every artifact should have one clear responsibility it can be judged against. Decision artifacts decide. Execution artifacts execute. Reference artifacts inform.

**Prefer:**
- Artifacts describable in one sentence
- Names that reveal responsibility
- Explicit handoffs between decision and execution

**Avoid:**
- Mixed policy, procedure, and reference content
- Work units that decide their own routing
- Broad catch-all files

---

### 4. One Owner Per Concern

Every rule, constraint, and definition has exactly one authoritative home. Before creating something new, find out whether an existing owner already covers it.

**Prefer:**
- A single owner for each rule, referenced from elsewhere
- Auditing existing sources before adding another
- Extending the rightful owner when it still fits

**Avoid:**
- Local copies of shared conventions
- Parallel or competing authorities for the same concern
- Creating a cleaner-looking duplicate

---

## Control And Safety

### 5. Make Behavior Explicit

Assumptions, success criteria, uncertainty, and stopping conditions should be stated rather than inferred. Critical decision points must be able to actually stop work until the required condition exists.

**Prefer:**
- Declared assumptions and visible success criteria
- Output artifacts that prove gated steps happened
- Ambiguity surfaced before action
- Blocking conditions with clear next steps when they fire

**Avoid:**
- Soft language for hard requirements
- Rules that only advise where they should gate
- Critical checks that can be skipped silently
- Compliance that depends on private memory instead of transcript evidence

---

### 6. Ask Before You Cut

Changes that can lose work, disrupt users, or reshape authority require explicit consent.

**Prefer:**
- Naming the risk before acting
- Explaining the intended safe outcome
- Treating consent as a requirement, scoped to what was approved

**Avoid:**
- Proceeding because a change seems obvious
- Hiding risk inside a larger change
- Treating approval for one change as approval for related changes
