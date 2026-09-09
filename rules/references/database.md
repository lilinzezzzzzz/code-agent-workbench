---
trigger: model_decision
description: Load for SQL or ORM access, joins, application-side data assembly, repositories, transactions, pagination, batching, locking, concurrency, query performance, or query memory and temporary-storage pressure.
---
# Database Access And Transaction Rules

Use these rules for database access and persistence behavior. Verify from
evidence the engine, version, workload, data volume, indexes, and transaction
model relevant to the current decision before relying on dialect-specific
behavior or making workload-dependent claims.

## Query Shape And Performance

- Read only the columns and rows needed by the contract. Bound user-facing and
  large-data reads with pagination, limits, or streaming; define a maximum page
  size and reject or cap unsafe input.
- For list, existence, and locking queries, prefer an explicit projection over
  loading an entire ORM entity. Inspect mapped types and generated SQL for
  unnecessary JSON, TEXT, BLOB, or other wide payloads, including implicit
  eager loads. When full entities are needed, establish that need from the
  contract and check that deferred access does not introduce N+1 queries.
  Document the reason only when it is non-obvious or affects a material
  trade-off; this does not introduce a separate approval step.
- Avoid N+1 queries and database calls inside per-item loops when a set-based,
  batched, preloaded, or bulk operation preserves semantics. If batching would
  break ordering, locking, error isolation, or memory limits, document the
  reason and bound the loop.
- Add ordering only when required by correctness, stable API behavior,
  pagination, or user-visible semantics. Include a unique tie-breaker for
  deterministic `LIMIT` or pagination; never rely on natural row order. Inspect
  implicit ORM/helper ordering; do not add a universal timestamp sort or switch
  sort columns as a memory fix without a matching contract and plan evidence.
- Treat deep offset pagination as a workload-dependent review signal. Prefer
  cursor/keyset pagination for hot or large changing datasets when clients can
  accept its navigation and consistency semantics.
- Inspect generated SQL. For material performance changes, use the target
  database's query plan and representative cardinalities; do not infer index
  use or improvement from ORM code alone.
- Account for connection-pool occupancy, query timeout, cancellation, result
  materialization, and memory—not only database execution time.

## Query Memory And Temporary Storage

- For new or materially changed queries with plausible resource risk, inspect
  the relevant generated SQL and available plans for costly sorts, DISTINCT,
  grouping, window functions, joins, and materialization. Select evidence from
  the affected operators and expected workload, including intermediate row
  counts and widths where relevant. Small results, pagination, and application
  streaming alone do not establish bounded server-side work, memory,
  temporary storage, or locks.
- For resource failures or regressions, inspect exact SQL and representative
  parameters, engine/version, schema/indexes, payload sizes, statistics, and an
  estimated plan first. Identify the costly operators and use safe runtime
  evidence to compare estimated and actual cardinalities, memory, spills, and
  waits where supported. Distinguish operator limits, overall memory pressure,
  and temporary-storage exhaustion; do not infer the cause from an error label
  such as MySQL 1038 alone or apply one engine's remedy to another.
- Reduce unnecessary projected data and intermediate rows where semantics
  permit, then evaluate access paths for filtering and ordering together,
  including tenant and soft-delete predicates. Consider sort direction,
  expressions, and engine-specific index behavior. An indexed sort column or
  primary key alone does not prove sort elimination. Treat composite indexes
  as candidates until supported by schema and plan evidence; follow
  `database-schema.md` when changing indexes.
- Preserve required ordering, complete results, aggregation, and consistency.
  Do not suppress failures by arbitrarily truncating results, removing DISTINCT
  or ORDER BY, or moving an unbounded sort/aggregation into application memory.
- For tables with wide fields, first determine whether the query needs those
  fields; if not, use a single query projecting only required columns. When
  wide payloads are needed alongside sorting, pagination, or broad filtering,
  prioritize evaluating two-phase fetching: select primary keys and necessary
  sort keys with required filters and bounds, then batch fetch payloads by
  those keys without repeating the wide-row database sort. Choose from plan,
  cardinality, payload-size, and round-trip evidence, not field types alone.
  A single-row primary-key detail lookup normally needs only one query.
  Restore the first query's order in application memory; IN does not preserve
  input order. Define missing-row behavior and bound payload bytes as well as
  key count. Avoid per-key fetches and apply the locking rules below.
- Split wide payloads into separate storage only when measured size, access
  frequency, or lifecycle warrants it, not merely because the type is JSON or
  large text. Account for batch loading, atomic updates, and migration; joining
  payloads back before a costly operator can reintroduce the same problem.
- Tune memory or workload concurrency when plan and workload evidence warrants
  it. Establish the engine/version's allocation model: limits may apply per
  operator, worker, query, or session, and concurrent demand can multiply.
  Do not equate MySQL sort_buffer_size with PostgreSQL work_mem. Prefer a
  narrowly scoped trial where supported, handle pooled
  connection setting restoration, and define rollback before broader changes.
  Preserve approval requirements for live configuration changes.
- Treat sorts and disk spills as measured costs, not automatic defects or
  guaranteed safe fallbacks. Where spills occur, account for temporary-space
  quotas/capacity, I/O latency, and concurrent usage as well as RAM; increasing
  an operator's memory allocation can worsen total memory pressure.
- For material resource changes, choose the smallest target-engine check
  capable of testing the claimed improvement. Include large payloads, skew,
  boundary cardinalities, or concurrency when the change or failure makes
  them relevant; do not require every dimension for every query. Reuse
  adequate existing evidence. Mocked ORM tests or another engine do not
  establish target-engine resource behavior. Execution-based plan tools such
  as EXPLAIN ANALYZE run the workload: use them and failure reproductions only
  in a safe test environment.
- If the target environment or evidence is unavailable, continue independent
  work within the requested scope. For review or diagnosis, deliver supported
  findings and identify unverified claims; for implementation, complete
  authorized local edits and applicable checks. Missing evidence blocks only
  the decision, execution, or claim that depends on it.

## Joins And Application-Side Assembly

- Follow the repository's established data-access strategy. When no convention
  exists, prefer bounded set-based queries and keyed application assembly when
  it improves ownership or service boundaries without harming correctness or
  resource use; do not prohibit a database join mechanically.
- Fetch each dataset with set-based queries such as bounded `IN` batches or
  equivalent bulk lookups. Select only required columns and never replace one
  database join with per-row queries or another N+1 pattern.
- Use keyed maps or grouped collections instead of nested O(n*m) scans. Define
  duplicate-key, missing-reference, one-to-many, ordering, and partial-data
  behavior explicitly so the in-memory result matches the business contract.
- Estimate row count, payload size, and peak memory before materializing data.
  Chunk, page, or stream bounded groups when needed; do not load an unbounded
  dataset into memory for application-side joining.
- Choose a database join when it better preserves consistency, ordering,
  filtering, aggregation, memory bounds, or observed performance. For material
  paths, compare representative query plans and application-side resource use
  rather than treating either strategy as universally preferred.

## Writes And Batching

- Prefer set-based or bulk writes when validation, hooks, audit behavior,
  returned values, and per-row error semantics remain correct. Chunk by
  parameter limits, transaction duration, lock footprint, and memory.
- Enforce business uniqueness and invariants in the database where the
  ownership model supports it. An application pre-check alone is race-prone.
  For relationship integrity, follow `database-schema.md`'s logical-reference
  policy; this rule does not require new physical foreign keys.
- Define partial-failure and retry behavior for bulk operations. Make resumable
  jobs checkpointed or idempotent rather than restarting an unbounded batch.

## Transactions And Concurrency

- Choose the transaction boundary from the business invariant. Keep it short,
  explicit, and free of user interaction or unrelated work.
- Keep external network I/O outside a transaction unless an established design
  bounds timeout, retry, idempotency, lock duration, and partial failure.
- Protect read-modify-write logic with an atomic statement, unique constraint,
  optimistic version check, or appropriate lock. Select isolation and lock
  mode from the anomaly being prevented.
- Acquire multiple locks in a stable order where practical. Retry deadlock or
  serialization failures only with bounded policy and a transaction safe to
  repeat.
- For SELECT ... FOR UPDATE, select only keys and state required by the
  invariant when possible, and inspect the access path and lock footprint.
  Result ordering alone is not proof of lock acquisition order. Before
  removing ORDER BY or splitting key selection, locking, and payload reads,
  preserve transaction ownership and account for concurrent inserts, updates,
  deletes, and revalidation under the actual isolation level. Do not introduce
  an unlocked selection window or chunk away required atomicity as a memory fix.
- When splitting a locking read, preserve the established protection across
  key selection and payload loading within the caller-owned transaction.
  Acquire required protection before exposing a selection race; do not
  assume that two statements in one transaction are sufficient. Verify that
  payload visibility meets the invariant and distinguish ORM refresh from
  database visibility. Cover pre-existing snapshots and lock waits when
  reachable through supported callers, reusing adequate existing tests.
- Define transaction ownership across helper and repository layers. Do not
  unexpectedly commit, roll back, or open a nested transaction inside a helper
  whose caller owns atomicity.
- Apply supported statement and transaction timeouts, propagate cancellation,
  and release rows, locks, cursors, sessions, and connections on every path.
