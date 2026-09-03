---
version: 3.0.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifesto/blob/main/plugins/agent-manifesto/IMPLEMENTATION.md
---

# Implementation

## Purpose

This document defines how to apply [MANIFEST.md](MANIFEST.md) when creating, reviewing, or adjusting an AI landscape.
It defines artifact boundaries and composition rules. Procedures live in `workflows/`.

---

## Framework Sources

- `MANIFEST.md`: values and principles
- `IMPLEMENTATION.md`: artifact and composition rules
- `workflows/*.yml`: framework procedures, including retirement
- `skills/*/SKILL.md`: reusable task-scoped policies
- `agents/*.md`: fresh-context responsibility templates
- `contracts/*.schema.json`: machine-readable data shapes

Framework sources are design inputs. Generated project artifacts must be self-contained and must not depend on this
repository remaining available.

---

## Generated Landscape

Create only the layers justified by current evidence.

### Context

Context records facts and preferences the model cannot reliably infer.

Possible contents:

- user role, business, audience, and vocabulary
- project purpose, architecture, commands, and authoritative sources
- voice, banned language, and output defaults
- preferred methodologies and quality expectations
- accepted assumptions and known exceptions

Separate personal context from team-shared project context. Do not commit private personal information merely because
it is useful to the user's local assistant.

Detailed context should be discoverable on demand. The root contract should point to it rather than reproduce it.

### Root Contract

The root contract is the smallest always-loaded brief for the selected tool.

It may contain:

- project identity and a map to authoritative context
- universal authority boundaries
- project-specific invariants that apply to nearly every task
- concise discovery pointers for available workflows and capabilities

It must not contain:

- task procedures
- generic reasoning advice
- a mandatory manager or routing ceremony
- duplicated reference documentation
- detailed policy that applies only to one kind of work

For a single-tool landscape, use that tool's native root file. For a multi-tool landscape, choose one canonical source
of shared intent and generate the smallest native adapter each selected tool requires. Verify current native discovery
behavior from official documentation during setup or review.

### Skills

A skill is an on-demand policy for one task-scoped concern in the main working context.

A skill defines:

- when the policy applies
- desired outcomes and important invariants
- project-specific constraints or preferred methodology
- relevant sources and expected evidence

A skill does not own cross-capability order, routing, or detailed reasoning. Use the Agent Skills `SKILL.md` format with
at least `name` and `description`, adapted to the selected tool's native discovery location.

Create a skill only when the concern recurs or when consistency materially matters. One skill owns one concern.

### Workflows

A workflow is a declarative procedure stored as YAML. It owns phases, order, dependencies, approvals, and failure
behavior. It may apply skills and assign a step to an agent.

Rules:

- validate every workflow against `contracts/workflow.schema.json`
- state a goal for every step
- omit `agent` when the main model should perform the step
- reference only skills, agents, and contracts that exist in the target landscape
- use contracts only for genuinely structured boundaries
- keep local problem solving out of the workflow
- express a real repetition with `for_each` and a real repair cycle with `retries` rather than burying either in a
  step's goal text
- prefer a short linear workflow; add dependencies, conditions, repetition, or retries only when the real procedure
  needs them
- do not require a manager node

Create a workflow for repeated ordered work, not for a one-off plan or a single action.

Execution semantics:

- `inputs` lists the files needed to start; referenced skills, agents, and contracts load only when their step
  becomes eligible
- a step without `needs` is an entry step
- a step becomes eligible when every named dependency completed, was skipped, or failed with `continue`
- evaluate `when` from visible repository and conversation state; skip the step when it is false
- `for_each` repeats the step once per item in the collection it names; the collection is resolved at run time and the
  step completes when every item is handled
- `approval: required` means the step cannot complete without an explicit user response
- `retries: N` allows up to N additional attempts when the result misses the step's goal and the shortfall is repairable
  inside the already-approved scope; repair between attempts belongs to the main model, never to a read-only agent
- `on_failure: stop` ends the workflow; `ask_user` pauses and resumes the step after clarification; `continue` records
  the failure and releases dependent steps; failure behavior applies only after `retries` is exhausted
- independent eligible steps may run in parallel only when they do not mutate overlapping state or require user input
- skill and agent references use their frontmatter `name`; contract references use the `.schema.json` basename

### Agents

An agent owns one recurring responsibility that materially benefits from fresh context.

Valid reasons include:

- an independent or unbiased review
- large or noisy exploration that should not consume the main context
- a bounded parallel responsibility
- restricted tools or permissions

An agent declares its responsibility, input boundary, authority, stopping conditions, and expected output. Add an
`output_contract` only when another consumer must parse or validate a structured result. It does not own orchestration
or reproduce shared policies. A one-off isolated task may use the tool's built-in subagent without creating a permanent
custom agent.

An adapted agent must preserve the source trigger, required inputs, responsibility, authority boundary, tool limits,
dependencies, stopping conditions, isolation rationale, exact vocabulary consumed by other procedures, and output
semantics. Keep the agent directory free of prose files: hosts that scan it load every Markdown file as an agent.

### Contracts

A contract is a machine-readable data shape for a structured boundary.

Use contracts for workflow definitions, agent results, or handoffs that another consumer must parse or validate. Do not
use contracts for conversational status reports, qualitative policy, or evidence that a human can assess directly.

The `change-proposal` contract carries the approved scope. Every workflow that changes files produces one before asking
for approval and treats it as the boundary for every later step: the file effects the user agreed to, whether each is
destructive or authority-expanding, the layer that owns each file, the external actions needing separate consent, the
paths that must stay local, and unverified assumptions. Record fingerprints for pre-existing working-tree changes so
they are ignored only while unchanged. An authority-expanding operation states its effects and locks the approved
post-change content hash; path approval alone cannot authorize an unmentioned permission or authority change.

Every step that changes files declares it, including documentation alignment. A step that edits files outside the
approved operations has left the boundary the user agreed to.

Prefer JSON Schema unless the selected runtime requires another standard. Human-readable YAML instances may validate
against JSON Schema.

### Deterministic Enforcement

Use settings, permissions, hooks, scripts, schemas, tests, or linters when a rule must hold regardless of model
judgment.

Examples:

- block forbidden version-control or deployment commands
- validate workflow YAML and landscape references with `scripts/validate.py`
- protect generated files
- run formatters or targeted checks

Install the landscape validator into the landscapes this framework creates. Enforcement that stays in the framework
repository does not protect the user's project.

Claude Code has its own `workflows` plugin component, meaning JavaScript orchestration scripts, unrelated to this
framework's declarative `workflows/*.yml`. Its default scan ignores non-script files, so the manifest leaves the field
unset: declaring it only to suppress the scan makes the host warn that the default folder is ignored.

Keep the human-readable policy as short as possible and point to the enforcement mechanism when that knowledge helps.

---

## Universal Components

Every landscape created or materially adjusted by the framework includes, when the selected tool supports them:

- the `brainstorm` skill for unresolved decisions with meaningful alternatives
- the `instruction-evaluator` agent for independent landscape review

Documentation maintenance is included when the project has an authoritative documentation surface and changes to that
surface are recurring.

Universal means broadly useful, not always loaded. These components remain on demand.

If the selected tool cannot define a native custom agent, run instruction evaluation in a separate fresh session when
possible. Otherwise report that independent evaluation was unavailable.

---

## Composition Rules

### Inspect Before Asking

Read the repository and existing landscape first. Distinguish evidence from inference and ask only questions whose
answers would change the result.

Do not ask about voice, banned words, software methodology, or other candidate concerns when they do not apply.

### Preserve Before Replacing

In an existing landscape:

- preserve useful native artifacts and established names
- identify the authoritative owner of each concern
- flag conflicts, duplication, stale scaffolding, and undiscoverable files
- ask before moving, renaming, deleting, merging, or replacing artifacts

Adjustment is not permission for wholesale migration.

### Keep Direction Proportional

Express SDD, TDD, review practices, and similar methodologies as task-scoped outcomes and invariants. Add procedural
workflow steps only when the user actually follows a repeatable sequence that should be preserved.

### Validate In Proportion To Risk

Use the project's real checks. Do not create conversational proof artifacts when test output, schema validation, a
diff, or direct inspection already provides the evidence.

Use an independent evaluator when the landscape itself changed. Add stronger behavioral evaluation only for complex or
high-risk workflows where representative failures justify it.

### Respect Scope

Discussion and review do not authorize edits. An approved proposal authorizes only its stated files and effects.

External actions such as commits, pushes, deployments, publication, messages, purchases, or production changes require
the user's explicit authority unless a pre-existing project policy clearly grants it.

Approved scope is recorded as a `change-proposal` and verified after implementation. Before proposing changes in a
dirty repository, capture the baseline to include as `preexisting_changes`:

```text
python3 scripts/validate.py . --snapshot
```

After implementation, compare the working-tree delta and locked content hashes with the approved operations:

```text
python3 scripts/validate.py . --proposal approved-change.json
```

The check reports unapproved changes, drift in pre-existing changes, mismatched approved hashes, and any staged path at
or below a `private_to_local` entry. A generated validator under `.claude/scripts/` discovers the project root
automatically; passing `.` remains explicit and portable.

---

## Maintenance

Review a landscape after a significant model or tool change and at least every six months.

For each instruction, determine whether it is:

- durable context
- user or project policy
- authority boundary
- temporary scaffolding

Test temporary scaffolding against a fresh minimal baseline. Remove it when representative work no longer benefits.
Keep a normal version-control history of deletions; do not maintain an always-loaded historical log.

The framework's own cases live in `evals/`. Run them after a model or tool change; a landscape that has drifted toward
ceremony fails the case that requires it to find nothing.

Removing the landscape entirely is a supported outcome, not a failure. `workflows/retire.yml` preserves durable
context, policy, and authority boundaries at a destination the user chooses before deleting anything.

---

## Acceptance

A landscape is ready when:

- the user can begin ordinary work without framework-specific ceremony
- always-loaded context contains only broadly relevant facts and boundaries
- selected tools can discover their native artifacts
- skills, workflows, agents, and contracts obey their responsibility boundaries
- workflows and structured outputs validate against their contracts
- non-negotiable restrictions are enforced mechanically where practical
- the independent instruction evaluator reports no unresolved blocking issue
- skipped or unavailable checks are reported honestly

Do not add an artifact merely to satisfy the shape of the framework.
