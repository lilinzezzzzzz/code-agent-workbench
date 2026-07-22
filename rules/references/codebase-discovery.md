---
trigger: model_decision
description: Load for non-trivial changes, reviews, bug investigations, unfamiliar modules, instruction discovery, blast-radius analysis, shared contracts, generated artifacts, or overlap with user work.
---
# Codebase Discovery Rules

Use these rules to gather enough verified context for a small, correct change
or a defensible review. Discovery is complete when the affected behavior,
constraints, consumers, verification path, and user-work overlap are known—not
when the whole repository has been read.

## Discovery Sequence

1. Establish the repository root, current workspace state, and target scope.
   Inspect `git status --short` and the relevant diff before touching a file
   that may already contain user changes.
2. Read the instruction chain from the repository root to the target path.
   Include narrower child instructions when a parent-rule change would affect
   them.
3. Find the source of truth with `rg`/`rg --files`, then read the target code,
   immediate callers and callees, representative tests, and the config or
   schema that constrains behavior. Do not infer behavior from names alone.
4. Trace the smallest complete path from input or caller to output, side
   effect, persistence, or external dependency. For bugs, compare the failing
   path with the expected contract and closest regression test.
5. Identify the repository's existing build, generation, lint, type-check, and
   test commands before inventing new commands or editing generated output.

## Blast-Radius Checklist

Check only categories relevant to the task, but do not skip a category merely
because it lives outside the target directory:

- Public APIs, SDKs, CLI flags, config keys, environment variables, wire
  formats, error codes, versioning, and compatibility shims.
- Persisted models, migrations, indexes, backfills, transactions, caches,
  queues, scheduled jobs, and generated artifacts.
- Auth, permissions, tenant boundaries, secrets, audit events, external
  services, billing, and deployment order.
- Cancellation, retry, timeout, idempotency, concurrency, resource ownership,
  large-data behavior, and latency-sensitive paths.
- Documentation, fixtures, examples, mocks, and downstream tests that encode
  the current contract.

For shared code, sample all materially different consumer classes rather than
only the nearest caller. For configuration or generated artifacts, locate the
consumer and source-of-truth generator before editing.

## Evidence And Conflict Handling

- When docs, tests, schemas, and implementation disagree, determine which is
  authoritative from runtime usage and repository conventions. Do not silently
  normalize the inconsistency; report compatibility implications.
- Before deleting or renaming symbols, files, fields, or routes, search static
  references and account for dynamic registration, reflection, generated code,
  external consumers, and persisted data where applicable.
- If required evidence depends on unavailable credentials, services, network,
  production data, or unsupported tooling, name the gap and avoid converting an
  assumption into a verified claim.

## Exit Criteria

Before editing or finalizing a review, be able to state:

- The files and instructions that define the current behavior.
- The intended behavior and affected compatibility or persistence surfaces.
- The planned files and why each must change.
- The smallest meaningful verification and any evidence that remains
  unavailable.
