# brainstorm_protocol.md

## Purpose

This document defines the canonical protocol for all brainstorming and discussion behavior across any project built with this framework.

This is a **reference document**, not a skill.
Skills reference this document. They do not redefine it.

---

# When Brainstorming Applies

Brainstorming applies whenever:
- a design decision must be made
- an architecture choice is unclear
- multiple valid approaches exist
- trade-offs need to be evaluated
- the user has not yet committed to a direction

Brainstorming does NOT apply:
- during execution phases
- after a decision is already made and confirmed
- for purely factual or informational questions

---

# Core Rules

## 1. One Question at a Time

Ask exactly **one question** per turn.

Never bundle multiple questions.
Never ask a question as a follow-up in the same message.

After asking → stop → wait for user input.

---

## 2. Always Provide Options

For every question, provide **2–3 concrete, comparable options**.

Options must be:
- distinct from each other
- actionable
- specific enough to compare

Never present vague or overlapping options.
Never present more than 3 options unless explicitly requested.

---

## 3. Always Highlight Trade-offs

For each set of options, explicitly state:
- risks of each option
- bottlenecks or edge cases
- what each option optimizes for
- what each option sacrifices

Do not present options as equally valid if they are not.
Prefer proven patterns when they exist — state the reasoning.

---

## 4. Stop and Wait

After presenting options:
- explicitly ask the user to choose or clarify
- **stop**
- do not continue to the next topic

The next question is asked only after the current decision is resolved.

---

## 5. Never Mix Brainstorming with Execution

During a brainstorming phase:
- no files are created
- no code is written
- no instructions are modified
- no implementation is proposed

Brainstorming produces decisions, not artifacts.
Execution begins only after brainstorming is explicitly complete.

---

## 6. The User Decides

The AI presents options and trade-offs.
The user makes the final decision.

The AI must never:
- assume a decision was made implicitly
- proceed without explicit user confirmation
- override a user's stated preference

---

## 7. Focus on High-Impact Decisions Only

Do not ask about:
- trivial details
- things already clearly established by the existing context
- preferences that do not affect architecture or behavior

Ask only about decisions that affect:
- task classification
- routing or orchestration
- review and validation policy
- reference documentation
- project scale assumptions
- level of modularity

---

## 8. Use Research Only When Necessary

Use external research only if:
- the decision depends on unknown or time-sensitive information
- multiple competing approaches require external validation

Do not research things that can be reasoned about from first principles.

---

# Phase Structure

When brainstorming is part of a multi-phase process (e.g., initial_prompt or evolution_prompt), brainstorming always occupies its own dedicated phase.

Rules:
- brainstorming phase must complete before execution phase begins
- no partial execution during brainstorming
- phase transition must be explicit and confirmed by the user

---

# Output of Brainstorming

At the end of a brainstorming phase, the AI must produce a **decision summary** before proceeding.

The summary must include:
- each decision made
- the option chosen
- any constraints or caveats noted by the user

The user must confirm the summary before execution begins.

---
