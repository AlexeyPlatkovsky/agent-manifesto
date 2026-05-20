---
version: 2.8.0
project: agent-manifest
url: https://github.com/AlexeyPlatkovsky/agent-manifest/blob/main/conventions/reference-docs.md
---

# reference-docs.md

## Purpose

This convention defines how generated or reviewed project reference docs are structured for selective loading and context control.

Reference docs store reusable project knowledge.
They inform work but do not enforce behavior.

---

# Reference Doc Structure

## 1. Identify Authoritative Doc Roots

The framework-standard shared location for generated reference docs is `.ai/docs`.

Projects may also keep authoritative docs in other folders, such as `docs/`, `documentation/`, product-specific directories, or tool-specific documentation roots.

When a project uses a non-standard documentation root, record or preserve that root in the project profile, root contract, or relevant docs index.

Do not move existing project docs into `.ai/docs` unless the user explicitly approves that structural refactor.

## 2. Use Purposeful Subfolders

Use subfolders when a doc set has multiple domains, systems, products, APIs, workflows, or source families.

Examples:
- `.ai/docs/api/`
- `.ai/docs/architecture/`
- `.ai/docs/domain/`
- `.ai/docs/operations/`

Do not flatten unrelated topics into one large document when stable subfolders would make selective loading easier.

## 3. Maintain A Docs Index

Every generated or reorganized `.ai/docs` tree must include `.ai/docs/README.md`.

Non-standard authoritative documentation roots should have an equivalent index when the doc set is large enough to require selective loading.

The index must identify:
- each doc or doc family
- the knowledge it contains
- stable anchors, IDs, or file paths for common lookup targets
- when an AI should read that doc

The index is a lookup aid.
It is not a root contract, routing artifact, policy layer, or source of behavioral rules.

## 4. Split Into Stable Sections

Large reference docs must be split into stable files or stable sections.

Use unique anchors or IDs for sections that agents may need to retrieve independently.

For API docs, each endpoint or closely related endpoint group should have a stable lookup target such as:
- file path
- method and route
- section anchor
- explicit endpoint ID

Prefer headings, IDs, and file names that remain stable across wording changes.

## 5. Read Narrowly First

Agents should inspect the relevant docs index before reading large reference docs unless the needed file or section is already known.

When a task needs reference knowledge, agents should:
- identify the smallest relevant doc, section, or line range
- read that narrow context first
- expand only when the narrow context is insufficient
- avoid full-file reads for large docs unless the task requires global consistency or broad refactoring

Full-doc reads are justified for:
- global documentation refactors
- consistency audits
- index repair
- tasks where cross-section dependencies are the subject of the work

## 6. Keep Docs Factual

Reference docs may contain:
- architecture facts
- command references
- API or data contracts
- domain vocabulary
- source locations
- operational notes

Reference docs must not contain:
- routing gates
- task execution procedures
- validation requirements
- agent responsibilities
- root policy

Put behavioral standards in conventions, execution details in skills, and sequencing in pipelines.

---

# Context Usage Reporting

For non-trivial work that used reference docs, a separate context usage report is optional but recommended.

Do not add columns to the `task-complete` closure table.
If included, place this report separately from the `task-complete` table.

Recommended format:

| Doc | Sections / Lines Read | Line Count | Reason |
|-----|------------------------|------------|--------|

Rules:
- report actual docs read, not docs that would have been ideal to read
- use section anchors, IDs, or line ranges when available
- include exact line counts when easy, or an honest approximation when exact counts are impractical
- summarize broad reads honestly when exact line counts are impractical
- omit the report for trivial tasks or when no reference docs were read
