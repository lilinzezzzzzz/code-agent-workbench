---
trigger: model_decision
description: Load for SQL or ORM access, join avoidance, in-memory data assembly, repositories, transactions, pagination, batching, locking, concurrency, or query-performance work.
---
# Database Access And Transaction Rules

Use these rules for database access and persistence behavior. Confirm the
target engine, version, workload, data volume, indexes, and transaction model
before relying on dialect-specific behavior.

## Query Shape And Performance

- Read only the columns and rows needed by the contract. Bound user-facing and
  large-data reads with pagination, limits, or streaming; define a maximum page
  size and reject or cap unsafe input.
- Avoid N+1 queries and database calls inside per-item loops when a set-based,
  batched, preloaded, or bulk operation preserves semantics. If batching would
  break ordering, locking, error isolation, or memory limits, document the
  reason and bound the loop.
- Add ordering only when required by correctness, stable API behavior,
  pagination, or user-visible semantics. Include a unique tie-breaker for
  deterministic `LIMIT` or pagination; never rely on natural row order.
- Treat deep offset pagination as a workload-dependent review signal. Prefer
  cursor/keyset pagination for hot or large changing datasets when clients can
  accept its navigation and consistency semantics.
- Inspect generated SQL. For material performance changes, use the target
  database's query plan and representative cardinalities; do not infer index
  use or improvement from ORM code alone.
- Account for connection-pool occupancy, query timeout, cancellation, result
  materialization, and memory—not only database execution time.

## Join Avoidance And In-Memory Assembly

- Avoid SQL/ORM joins by default. Prefer querying each table independently in
  bounded batches, then assemble related data in application memory by stable
  logical-reference keys.
- Fetch each dataset with set-based queries such as bounded `IN` batches or
  equivalent bulk lookups. Select only required columns and never replace one
  database join with per-row queries or another N+1 pattern.
- Use keyed maps or grouped collections instead of nested O(n*m) scans. Define
  duplicate-key, missing-reference, one-to-many, ordering, and partial-data
  behavior explicitly so the in-memory result matches the business contract.
- Estimate row count, payload size, and peak memory before materializing data.
  Chunk, page, or stream bounded groups when needed; do not load an unbounded
  dataset into memory for application-side joining.
- If neither bounded in-memory assembly nor a denormalized read model can meet
  correctness or resource limits, use a database join only with an explicit
  reason, representative query plan, bounded result, and observed performance.

## Writes And Batching

- Prefer set-based or bulk writes when validation, hooks, audit behavior,
  returned values, and per-row error semantics remain correct. Chunk by
  parameter limits, transaction duration, lock footprint, and memory.
- Enforce business uniqueness and invariants in the database where the
  ownership model supports it. An application pre-check alone is race-prone.
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
- Define transaction ownership across helper and repository layers. Do not
  unexpectedly commit, roll back, or open a nested transaction inside a helper
  whose caller owns atomicity.
- Apply supported statement and transaction timeouts, propagate cancellation,
  and release rows, locks, cursors, sessions, and connections on every path.
