---
version: 2.8.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/protocols/brainstorm.md
implementation: mandatory
requires_when:
  - open design decisions with multiple valid paths
  - clarification requires trade-off evaluation
  - setup or profile clarification requires choosing between meaningful options
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
- wait for user confirmation of the decision summary before execution begins
- emit a visible decision-summary artifact before execution begins

The generated project skill may add minimal project-specific adaptation, examples, or terminology.
It must not weaken these rules.

---

# When Brainstorming Applies

Brainstorming applies only when a `requires_when` trigger from this protocol's frontmatter is present:
- open design decisions with multiple valid paths
- clarification requires trade-off evaluation
- setup or profile clarification requires choosing between meaningful options

Brainstorming does not apply:
- during execution
- after a decision is already confirmed
- for purely factual questions that do not require choosing between meaningful options

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

For factual setup or profile fields, always provide a free-form correction path so the user can supply the actual role, tool, path, or project fact when the listed options are incomplete or inaccurate.

## 3. Always Highlight Trade-Offs

State what each option optimizes for, what it sacrifices, and what risks or bottlenecks it carries.

Do not present options as equally valid when user-stated requirements, framework constraints, risk, context weight, or operational feasibility make one option materially stronger or weaker.

For setup or profile clarification, keep trade-off notes brief and practical. Explain the likely impact of each option without expanding factual profile capture into broad design analysis.

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
- capability triggers

---

# Output Contract

At the end of a brainstorming phase, produce a decision summary that includes:
- each decision made
- the selected option
- any caveats or constraints noted by the user

Execution may begin only after the user confirms that summary.

The decision summary must begin with the project-local capability name:

`Skill: <brainstorm-capability-name> - output below`
