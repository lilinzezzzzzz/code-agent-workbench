---
trigger: model_decision
description: Load when creating, materially updating, or reviewing technical Markdown documents such as architecture docs, implementation plans, runbooks, ADRs, checklists, and rollout or status docs.
---
# Markdown Documentation Rules

Use these rules to keep technical documents accurate, decision-oriented, and
maintainable. Follow a repository's more specific documentation convention
when one exists.

## Establish The Document Contract

- Identify the document type, intended readers, and the decisions or actions it
  must support before choosing its structure.
- State the document's responsibility, scope, and non-goals when ambiguity
  could cause it to overlap adjacent documents or imply unsupported behavior.
- Identify authoritative sources such as code, schemas, configuration, tests,
  generated specifications, or observed runtime evidence. Link to them instead
  of copying details that are likely to drift.
- Add status, owner, review date, or last-calibrated metadata only when the
  project will maintain it. Mark obsolete documents as superseded and link to
  the replacement rather than leaving two apparent sources of truth.

## Separate Truth From Intent

- Distinguish current behavior, target design, planned work, assumptions, and
  open questions. Do not describe a proposed design as already implemented.
- Support current-behavior claims with the best available source of truth. If
  code, configuration, tests, and documentation disagree, expose the conflict
  instead of silently choosing or normalizing one representation.
- Qualify observed results with the relevant environment, profile, version,
  date, and verification scope. Do not generalize a local or partial result to
  untested environments or end-to-end behavior.
- Use explicit uncertainty such as "planned", "inferred", or "not verified"
  when evidence is incomplete; do not convert intent or code presence into a
  verification claim.

## Match Structure To Document Type

| Document type | Decisions the document should support |
| --- | --- |
| Architecture | Boundaries, current or target topology, component responsibilities, interactions, invariants, failure semantics, constraints, and evolution triggers |
| Implementation plan | Goals and non-goals, phases and dependencies, tracked status, acceptance gates, verification, rollback conditions, and definition of done |
| Runbook | Preconditions and safety checks, ordered operations, expected signals, failure handling, rollback, and escalation |
| ADR | Context, decision, alternatives considered, trade-offs, consequences, status, and superseding decision |
| Investigation | Question, known constraints, evidence, candidate explanations or options, conclusion, uncertainty, and follow-up work |

Treat this table as a set of decision concerns, not mandatory section names.
Omit concerns that do not apply and do not force every document into one
template.

## Choose Lists By Meaning

| Syntax | Use when | Do not use merely because |
| --- | --- | --- |
| `- [ ]` / `- [x]` | The document owns an actionable, independently verifiable completion state | An action is mentioned or a procedure has not run yet |
| `1.` | Order, dependency, priority, or later reference by step number matters | The items happen to be actions |
| `-` | Items are peers and reordering them does not change meaning | The section contains multiple lines |

- Mark an item `[x]` only when repository state, command output, or observed
  runtime evidence supports completion. Keep partial work `[ ]` and describe
  completed and remaining portions, or split it when each part is independently
  useful to track.
- Write each checkbox as one verifiable outcome. Do not combine unrelated
  actions whose completion can diverge.
- Keep one list meaning at each nesting level. Nest conditions, explanations,
  commands, and evidence under the item they qualify; use a nested checkbox
  only for an independently maintained state.
- Keep ordered-list numbers sequential when readers may cite step numbers, and
  renumber them after inserting, removing, or reordering steps.

## Make Evidence And Examples Usable

- Prefer exact repository-relative paths, symbols, configuration keys, API
  fields, commands, and observable outcomes over vague descriptions. Validate
  links and heading anchors after moving or renaming content.
- Add a language identifier to fenced code blocks. State whether an example is
  runnable, illustrative, or pseudocode when readers could reasonably confuse
  them.
- For runnable commands, include material prerequisites, working directory or
  profile, and expected success signal. Do not include real credentials,
  personal data, or sensitive internal payloads in examples or output.
- Use tables for repeated-field mappings or comparisons, not long narrative.
  Use diagrams only when relationships, sequence, ownership, or state change
  are clearer visually than in concise prose.
- Explain each diagram's purpose in text and keep component names, boundaries,
  directions, and current-versus-target status consistent with the document.
  Describe important failure paths or transaction boundaries in prose when the
  diagram omits them.
- Use one term for one concept and explain non-obvious abbreviations on first
  use. Preserve exact identifiers when translation would reduce precision.

## Keep Documents Consistent

- Give each fact or completion state one canonical owner. Reference that owner
  from adjacent documents instead of duplicating volatile details.
- When a plan changes, update its summary, task state, ordered steps,
  dependencies, acceptance criteria, verification, rollback, and completion
  definition wherever they are affected.
- Do not repeat one status across prose, task lists, and tables unless one is
  explicitly authoritative and the document keeps the others synchronized.
- Keep heading hierarchy coherent and remove stale instructions or examples
  when the underlying contract changes. Preserve historical detail only when
  it supports audit, migration, rollback, or an explicit decision record.
- Do not add a table of contents, metadata block, fixed section set, or repeated
  summary by default; add it only when it improves navigation or decisions and
  can be maintained.
