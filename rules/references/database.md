---
trigger: model_decision
description: Load for SQL or ORM queries, repositories, transactions, pagination, locking, or query-performance tasks.
---
# Database Access And Transaction Rules

Use these rules when work touches database access, repositories or DAOs,
queries, transactions, pagination, locking, or persistence performance.

## Query And Persistence

- Identify expected row counts, access patterns, existing indexes, caller
  latency requirements, and ordering contracts before changing a query.
- Prefer explicit, bounded reads. Avoid unbounded `SELECT` in user-facing or
  large-data paths; use an explicit `LIMIT` or a bounded streaming pattern.
- Treat an offset greater than 1000 as a review threshold, not proof of a
  performance defect. For hot or large-data paths, prefer cursor/keyset
  pagination unless an actual query plan and workload justify deep offset
  pagination.
- Do not add `ORDER BY`, ORM `.order_by()`, default model ordering, or
  relationship ordering unless sorting is required for correctness, stable
  API behavior, pagination, top-N/latest/oldest semantics, or user-visible
  ordering.
- When deterministic order is required, make it explicit and include a stable
  tie-breaker for pagination or `LIMIT`; never rely on database natural order.
- Inspect generated SQL and use the target database's query-plan tooling for
  material performance changes. Do not infer index use from ORM code alone.

## Transactions And Concurrency

- Keep transaction boundaries explicit and as short as correctness permits.
  Do not keep a transaction open across user interaction or unrelated work.
- Keep external network I/O outside transactions unless an existing pattern
  defines timeout, retry, idempotency, and partial-failure handling.
- Protect read-modify-write invariants with an atomic statement, optimistic
  version check, or explicit lock; an application-side pre-check alone does
  not prevent concurrent writes.
- Choose isolation level and lock mode from the invariant being protected.
  Acquire multiple locks in a stable order where practical to reduce
  deadlocks.
- Retry deadlocks or serialization failures only when the project has a
  bounded retry policy and the transaction is safe to repeat.
- Apply query and transaction timeouts where supported, preserve cancellation,
  and always release sessions, connections, cursors, and locks on failure.
