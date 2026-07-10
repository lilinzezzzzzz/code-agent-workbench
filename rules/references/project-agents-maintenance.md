---
trigger: model_decision
description: Load for creating, updating, reviewing, deleting, or syncing global agent rules, project AGENTS.md files, nested instructions, reference routing, or durable repository guidance.
---
# Agent Instruction Maintenance Rules

Use these rules for global instruction sources, project `AGENTS.md` files,
nested agent guidance, and their on-demand references. Instruction files are an
execution interface: optimize for correct agent decisions, not exhaustive
documentation.

## Decide What Belongs

Add or retain a rule only when it is durable, actionable, and likely to change
future behavior. Prefer concrete invariants, commands, ownership boundaries,
compatibility constraints, and confirmation gates.

Exclude or move elsewhere:

- Generic advice already supplied by the platform or enforced by formatter,
  linter, type checker, tests, schema, or CI.
- Personal preference presented as universal correctness without an explicit
  fallback or project-override rule.
- Transient task notes, long tutorials, exhaustive examples, rationales that
  do not affect a decision, and repeated reporting instructions.
- Rules the agent cannot observe, verify, or execute.

## Scope And Placement

- Read the applicable instruction chain and affected child instruction files
  before editing a parent rule.
- Put cross-project safety, precedence, authorization, and reference-routing
  rules in the global always-on file. Keep it small because every technical
  turn pays its context cost.
- Put language, framework, database, API, Git, verification, and specialized
  workflows in narrowly triggered references or skills.
- Put repository-specific commands, architecture, ownership, generated-file
  rules, and local exceptions in the narrowest project `AGENTS.md` that covers
  the affected paths. Child rules specialize or override; they do not repeat
  parent rules.
- Use project documentation for explanations and onboarding. Agent
  instructions should point to the source of truth rather than duplicate it.

## Wording And Conflict Design

- Write imperatives with an observable trigger and outcome. State the scope of
  strong terms such as `must`, `never`, and `always`; use them only for genuine
  invariants or safety boundaries.
- Pair preferences with their override condition, for example “follow the
  repository; for greenfield work prefer X when Y holds.”
- Give each rule one canonical owner. The always-on file routes to domain
  references; references should not repeat global safety and reporting rules.
- Resolve contradictions explicitly. Use the standard hierarchy of platform
  and safety rules, current user intent, nearest local instructions, broader
  project instructions, then global defaults.
- Preserve compatibility notes when deleting or relaxing rules. A policy
  change affecting data, security, public APIs, deployment, billing, or team
  ownership requires explicit user or team direction.

## Reference Maintenance

- Keep each reference focused on one decision domain and independently
  understandable after the always-on file routes to it.
- Keep filename, frontmatter description, always-on trigger matrix, test
  prompts, and user-facing documentation aligned.
- Avoid reference chains unless the second file is required only for a narrow
  branch. The always-on router should select the normal combination directly.
- When trigger overlap is intentional, divide responsibility clearly—for
  example discovery determines affected surfaces, execution coordinates work,
  and verification evaluates claims.

## Validation And Reporting

- Inspect the final diff for duplicate directives, conflicting absolutes,
  broken paths, stale filenames, over-broad triggers, and rules that cannot be
  tested.
- Verify frontmatter, headings, reference resolution, trigger cases, and at
  least one negative case that should not over-load references.
- Report material policy changes separately from editorial compression,
  including any preference that was relaxed or made project-dependent.
