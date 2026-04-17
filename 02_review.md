# 02_review.md — Instruction System Review

## Context Required

Before starting, ensure the following files are available in this session:
- `MANIFEST.md` — canonical source of truth
- `brainstorm_protocol.md` — canonical brainstorming behavior
- Your full instruction system: `AGENTS.md`, all skills, workflows, agents, and reference docs

If any are missing, stop and ask the user to provide them.

---

## Purpose

Your task is to validate that the current instruction system fully complies with `MANIFEST.md` principles.

This is NOT an implementation task.
This is a strict audit and verification process.

Assume the system is **wrong until proven correct**.
Be critical, not optimistic.
Do not suggest fixes before completing the audit.

---

## Working Mode

Work in exactly 4 phases. Do not skip or merge phases.

1. **Audit** — full analysis against MANIFEST principles
2. **Clarification** — resolve genuine ambiguities with the user
3. **Final Validation** — verdict and minimal fix plan
4. **Implementation & Verification** — apply fixes and verify results (only when user requests)

During Clarification: follow `brainstorm_protocol.md` exactly.
Do NOT modify files during Phases 1–3.
Do NOT suggest implementation until Phase 3.

---

## Phase 1 — Audit

Read all provided instruction files. Validate each against MANIFEST principles.

---

### 0. Root Contract Presence

This check must be performed first.

- verify that `AGENTS.md` exists and is readable
- verify that it acts as the root operational contract
- verify that routing and capability declarations are visible from `AGENTS.md`
- verify that execution details are delegated to skills, workflows, and agents rather than embedded in the root file

Any failure here must appear in the violations list.

---

### 1. Context Minimization

- Is the root context (AGENTS.md) minimal?
- Is anything unnecessarily always-loaded?
- Are skills, workflows, and reference docs on-demand only?

---

### 2. Separation of Policy and Execution

- Does AGENTS.md contain only policy (WHAT / WHEN), not execution (HOW)?
- Exception: small projects may contain inline routing logic — is it minimal and scoped correctly?
- Are procedures confined to skills and workflows?
- Is any execution logic embedded in AGENTS.md beyond the permitted inline routing?

---

### 3. Progressive Disclosure of Complexity

- Is complexity introduced only when needed?
- Does the system start from direct execution and escalate appropriately?
- Are subagents used only where genuinely justified?
- Is the system over-engineered relative to the project size?

---

### 4. No Duplication

Check for duplicated rules across:
- AGENTS.md and skills
- skills and workflows
- multiple skills
- reference docs and skills

Any rule that exists in more than one place is a violation.

---

### 5. Responsibility Boundaries

- Does each file have exactly one responsibility?
- Do any skills contain orchestration logic?
- Do any workflows contain implementation details?
- Does AGENTS.md contain execution steps beyond permitted inline routing?
- Does the manager skill (if present) duplicate AGENTS.md?

---

### 6. Composability

- Are skills atomic and self-contained?
- Are workflows pure orchestration (referencing skills, not redefining them)?
- Are components reusable independently?

---

### 7. Determinism

- Are critical behaviors explicitly defined?
- Is any behavior left to "AI will figure it out"?
- Are routing decisions unambiguous?

---

### 8. Routing Language Enforcement (Critical)

This is the most commonly violated principle. Routing rules that read as guidance are non-compliant regardless of intent.

**Check for each routing rule in AGENTS.md:**

- Is the language imperative? (`STOP`, `MUST`, `DO NOT`) — or merely descriptive? (`should`, `route via`, `recommended`)
- Does the rule specify the exact next action? (load X skill, invoke Y agent) — or only the outcome? (use workflow, follow process)
- Does a routing gate appear **before** the capability registry at the top of AGENTS.md?
- Is "trivial" explicitly defined? Or is it left to AI interpretation?
- Are completion gates (validation, review) mandatory or optional?

**Non-compliant patterns — flag as violation:**
- Classification tables presented without blocking language
- "Should", "recommended", "route via" without a STOP instruction
- Routing logic buried in the capability registry instead of leading AGENTS.md
- Skills listed as "use for X" when they are mandatory for X

**Compliant pattern — required:**
- Explicit STOP before any non-trivial action
- Named skill/agent to load immediately
- Explicit statement that implementation must not begin until routing resolves

If routing language is descriptive rather than imperative → **Critical violation**.
If routing gate is missing from top of AGENTS.md → **Critical violation**.
If completion gates are optional rather than mandatory → **Major violation**.

---

### 9. Brainstorm Skill (Mandatory)

- Does a brainstorm skill exist?
- Is it registered in AGENTS.md?
- Does it reference `brainstorm_protocol.md` without redefining it inline?
- Is it correctly scoped (discussion only, not execution)?

If the brainstorm skill is missing → this is a **Critical violation**.

---

### 10. Routing Capability Requirements

First, determine the project size from context (contributor count, domain count, workflow complexity).


If the manager skill is missing on a medium or large project → this is a **Critical violation**.

If the project is **medium or large**:
- Is there either a dedicated manager skill OR another concrete routing capability named in AGENTS.md?
- Is the non-trivial routing target unambiguous?
- Are non-trivial tasks blocked on routing instead of being executed directly?
- If a manager skill exists, does it satisfy the large-project checks above except where scale makes extra structure unnecessary?

If project routing is ambiguous or unnamed → **Major violation**.

If the project is **small**:
- Is the inline routing in AGENTS.md minimal and correctly scoped?
- Is there a manager skill present that is not needed? (over-engineering signal)

---

### 11. Execution Matrix Application

- Is the execution matrix from MANIFEST translated into mandatory gate language rather than left as a table?
- Are trivial tasks explicitly allowed to proceed directly?
- Are non-trivial tasks blocked until the named routing capability is loaded?
- Are high-risk or system-level tasks routed through stronger validation or review paths?

---

### Architecture Validation

- Does the system complexity match the project size?
- Is there unnecessary manager / workflow / subagent infrastructure?
- Is routing logic centralized correctly?
- Are subagents used only when context isolation is genuinely beneficial?

---

### Context Efficiency

- Are skills modular and loaded on demand?
- Are workflows lightweight?
- Are reference docs used correctly (not always loaded)?
- Are there any large monolithic files that should be split?

---

### Risk-Based Execution

- Is the execution matrix from MANIFEST actually applied?
- Are high-risk tasks routed through review loops?
- Are trivial tasks handled directly without unnecessary overhead?

---

## Phase 1 Output

Provide:

### Routing Gate Report

For the main routing contract found in `AGENTS.md`:

| Location | Status | Named Capability | Notes |
|----------|--------|------------------|-------|
| ... | Valid / Ambiguous / Missing | ... | ... |

### Compliance Score
A score from 0 to 100 reflecting overall alignment with MANIFEST.

### Violations List

Group by severity:

**Critical (must fix before system is usable):**
- List each violation with: location, principle violated, description

**Major (significant risk or inconsistency):**
- List each violation with: location, principle violated, description

**Minor (low impact, worth fixing eventually):**
- List each violation with: location, principle violated, description

### Suspicious Areas
List anything that is unclear, potentially risky, or could be interpreted multiple ways.

### Over-Engineering Signals
List any complexity that appears unjustified by the project's actual scale.

### Under-Engineering Risks
List anything that is dangerously absent given the project's apparent needs.

---

STOP after Phase 1 output.
Do not proceed to Phase 2 until the user acknowledges the audit results.

---

## Phase 2 — Clarification

Resolve genuine ambiguities identified in Phase 1.

Ask questions ONLY if:
- a rule interpretation is unclear
- the design intent is ambiguous
- multiple valid interpretations exist and the choice affects the fix plan

Follow `brainstorm_protocol.md` exactly:
- one question at a time
- 2–3 concrete options per question
- stop and wait after each question

Do NOT ask about:
- things clearly established by the repository
- violations that are unambiguously wrong
- trivial details

Focus only on high-impact ambiguities that affect the fix plan.

If there are no genuine ambiguities → skip Phase 2 and proceed directly to Phase 3.
State explicitly that no clarification is needed and why.

---

## Phase 3 — Final Validation

After clarification (or if Phase 2 was skipped):

---

### Final Compliance Score

Revised score after clarification, with brief justification.

---

### Final Verdict

Choose exactly one:
- **Compliant** — system fully follows MANIFEST, no fixes required
- **Conditionally Compliant** — minor issues present, system is functional but should be improved
- **Non-Compliant** — critical or major violations present, system must be fixed before relying on it

---

### Minimal Fix Plan

IMPORTANT:
- Do NOT propose a full redesign
- Do NOT propose nice-to-have improvements
- Only propose the minimum changes required to reach compliance

For each required fix:
- **File:** which file to change
- **Issue:** what is wrong
- **Fix:** exactly what change is needed
- **Severity:** Critical / Major / Minor

Order fixes by severity. Address Critical first.

---

### Structural Correctness Summary

Confirm or deny each of the following:

- [ ] `AGENTS.md` is present and acts as the root operational contract
- [ ] No duplication exists across files
- [ ] Responsibility boundaries are clear and enforced
- [ ] Context is minimal — nothing unnecessary is always-loaded
- [ ] Layering is correct — policy in AGENTS.md, execution in skills/workflows
- [ ] Complexity matches project scale — no over or under engineering
- [ ] Routing gates use imperative blocking language — not descriptive guidance
- [ ] Routing gate appears at the top of AGENTS.md before capability registry
- [ ] Trivial task classification is explicitly defined, not left to AI judgment
- [ ] Completion gates (validation, review) are mandatory, not optional
- [ ] Brainstorm skill is present, correctly scoped, and registered
- [ ] Brainstorm protocol is referenced, not duplicated
- [ ] Large and medium projects include a manager skill or name an explicit routing capability for non-trivial work
- [ ] Execution matrix is applied through mandatory routing and completion gates

If any item cannot be confirmed → it must appear in the fix plan.

---

STOP after Phase 3 output.
Do not proceed to Phase 4 until the user explicitly requests implementation.

---

## Phase 4 — Implementation & Verification

This phase activates ONLY when the user approves the fix plan and requests implementation.

### 4a. Apply Fixes

Apply each fix from the Phase 3 Minimal Fix Plan, in severity order (Critical first).

### 4b. Verify Every Changed File

After ALL fixes are applied:

1. **Structural check**: Check every created or modified file for errors (syntax, missing required fields, invalid frontmatter). Any error must be fixed before proceeding.
2. **Content check**: Re-read each modified file and verify:
   - YAML frontmatter is present and valid (for skill/agent files)
   - All internal references point to correct paths
   - No content was accidentally removed or corrupted
3. **Re-run Structural Correctness Summary**: Go through every checkbox from Phase 3 against the actual file state. Confirm each item passes.

### 4c. Verification Report

```
## Verification Report

### Files Changed
| File | Action | Structural Check | Content Check |
|------|--------|-----------|---------------|
| ... | created / modified | pass / fail | pass / fail |

### Structural Correctness (post-fix)
[Re-run the Phase 3 checklist with updated status]

### Revised Compliance Score
[New score with justification]

### Issues Introduced by Fixes
[List any, or "None"]
```

If any verification step fails → fix before reporting completion.
Do NOT declare implementation complete until all checks pass.

---

## Quality Bar

The system is valid ONLY if:

- MANIFEST principles are fully respected
- `AGENTS.md` remains the root operational contract
- No duplicated logic exists
- Context is minimal
- Complexity matches project scale
- Routing gates use imperative blocking language and appear before capability registry
- Non-trivial routing is explicit, blocking, and unambiguous
- Brainstorm skill is correctly implemented
- Manager skill is correctly implemented where project size requires it
- System behavior is understandable from `AGENTS.md` alone

If any of these fail → system is NOT compliant.

---

## Critical Rule

If unsure about anything:
- do not assume
- ask in Phase 2

Validation without certainty is invalid.
