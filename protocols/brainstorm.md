---
version: 1.5.4
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/protocols/brainstorm.md
implementation: mandatory
applies_to:
  - small
  - medium
  - large
---

# brainstorm.md

## Purpose

This protocol defines canonical brainstorming behavior for framework-driven projects.

It is a framework input.
Project skills derived from it must be standalone project artifacts.

---

# Mandatory Implementation Rules

Any project skill derived from this protocol must:
- preserve the one-question-at-a-time contract
- present 2-3 concrete options for every question
- surface trade-offs and risks explicitly
- stop and wait after each question
- keep brainstorming separate from execution
- end the brainstorming phase with a decision summary before execution begins

The generated project skill may add minimal project-specific adaptation, examples, or terminology.
It must not weaken these rules.

---

# When Brainstorming Applies

Brainstorming applies when:
- a design decision is still open
- multiple valid approaches exist
- trade-offs need explicit evaluation
- the user has not committed to a direction yet

Brainstorming does not apply:
- during execution
- after a decision is already confirmed
- for purely factual questions

---

# Core Rules

## 1. One Question at a Time

Ask exactly one question per turn.

Do not bundle questions.
Do not ask a follow-up in the same message.

## 2. Always Provide Options

For every question, provide 2-3 concrete, comparable options.

Options must be:
- distinct
- actionable
- specific enough to compare

## 3. Always Highlight Trade-Offs

State what each option optimizes for, what it sacrifices, and what risks or bottlenecks it carries.

Do not present options as equally valid when they are not.

## 4. Stop and Wait

After asking the question:
- explicitly ask the user to choose or clarify
- stop
- wait for input before moving on

## 5. Never Mix Brainstorming with Execution

During brainstorming:
- do not create files
- do not edit instructions
- do not implement

Brainstorming produces decisions, not artifacts.

## 6. The User Decides

The AI presents options and trade-offs.
The user makes the decision.

Do not assume a decision was made implicitly.

## 7. Focus on High-Impact Decisions

Ask only about decisions that materially affect:
- routing
- orchestration
- validation
- structure
- reusable documentation
- project scale assumptions

---

# Output Contract

At the end of a brainstorming phase, produce a decision summary that includes:
- each decision made
- the selected option
- any caveats or constraints noted by the user

Execution may begin only after the user confirms that summary.
