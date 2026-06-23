---
trigger: model_decision
description: Load for non-trivial code changes, reviews, bug investigations, unfamiliar modules, local instruction discovery, blast radius analysis, or tasks that may overlap with user work.
---
# Codebase Discovery Rules

Use these rules before planning, reviewing, editing, or testing non-trivial
technical work. The goal is to gather enough verified local context to make a
small, correct change without overwriting user work or missing compatibility
constraints.

## When To Load

- Load this reference for unfamiliar modules, bug investigations, code
  reviews, multi-file changes, local instruction discovery, blast-radius
  analysis, or any task that may overlap with uncommitted user work.
- Also load it when touching shared helpers, public APIs, persisted data,
  generated artifacts, build/test workflows, or behavior that is only clear
  after tracing callers and tests.
- Trivial read-only answers and narrow single-file documentation edits may
  skip deeper discovery unless correctness, security, data safety, or user
  work preservation depends on it.

## Minimum Context

- Check workspace state before edits when changes may overlap with user work:
  inspect `git status --short`, and inspect relevant diffs before modifying
  files that are already changed.
- Discover local instructions from the repository root down to the target
  path, such as `AGENTS.md` files or project rule directories. Prefer
  project-local instructions and conventions over global defaults unless
  correctness, security, or data safety would be weakened.
- Use fast local search first, such as `rg` and `rg --files`, then open only
  the files needed for the task. Avoid inferring behavior from filenames,
  route names, or test names alone.
- Read files directly involved in the requested change, plus immediate
  callers, callees, representative tests, fixtures, config, schemas, docs,
  and generated-artifact sources that constrain the behavior.
- For bug investigations, read the failing path, the expected contract, and
  the closest regression tests before proposing or applying a fix.
- For code reviews, compare the changed behavior against the relevant
  contracts, callers, tests, and persistence or API boundaries before listing
  findings.

## Blast Radius

- Identify public APIs, SDK surfaces, CLI flags, config keys, environment
  variables, persisted formats, message schemas, migrations, generated
  artifacts, queues, scheduled jobs, external services, auth, permissions,
  caching, concurrency, and performance-sensitive paths before changing
  behavior.
- For shared code, trace the important call paths and representative tests
  before editing.
- For configuration or workflow changes, inspect the commands, scripts, CI
  jobs, and documentation that consume the changed file.
- For database or persistence changes, identify migrations, schema models,
  indexes, transactions, backfills, compatibility shims, and downstream read
  paths before editing.
- For API or integration changes, identify request/response contracts, error
  codes, idempotency behavior, retries, timeouts, auth context, and versioning
  expectations.
- For generated files, identify the source-of-truth generator and regenerate
  through the project command when practical. Do not hand-edit generated
  output unless the project explicitly supports it.

## User Work Protection

- Treat uncommitted changes as user work unless you created them in the
  current task. Do not overwrite, revert, delete, or reformat unrelated
  changes.
- If a target file already contains unrelated user edits, apply the smallest
  patch around the required lines and preserve the surrounding content.
- If user edits make the requested change ambiguous or unsafe, stop and ask
  only after gathering enough context to explain the conflict concretely.
- Before removing dead code, renaming public symbols, or relaxing behavior,
  check references with local search and understand compatibility impact.

## Decision Points

- Ask only when missing information affects correctness, data safety, or API
  compatibility, or when an action would require credentials, external
  service mutation, destructive commands, or broad policy changes.
- For low-risk gaps, choose the conservative option and state the assumption.
- If no project convention exists, use the global defaults from `AGENTS.md`.
- If a nearby issue is out of scope, mention it as a follow-up unless it
  causes incorrect behavior in the current change or is a trivial fix in the
  same function.
- If docs, comments, tests, and implementation disagree, prefer verified
  executable behavior for the immediate change and report the inconsistency.

## Exit Criteria

Before planning edits or finalizing a review, be able to name:

- The files and local instructions that constrain the task.
- The affected contracts, persisted data, generated artifacts, or external
  integrations, if any.
- The representative tests or verification commands that cover the changed
  behavior.
- Any assumptions, intentionally skipped references, and remaining risk.
