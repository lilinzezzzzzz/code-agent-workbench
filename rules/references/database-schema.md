---
trigger: model_decision
description: Load for database schema, DDL, persisted models, columns, indexes, logical foreign keys, constraints, migrations, or backfills.
---
# Database Schema And Migration Rules

Use these rules when work touches persisted models, schema design, DDL,
columns, indexes, logical relationships, migrations, or backfills.

## Schema Field Design

- Identify existing schema contracts, external readers, supported database
  engines and versions, deployment order, and rollback requirements before
  changing persisted structure.
- Use an explicit string length when the business contract, target dialect,
  validation boundary, or index design requires one. Use the database-native
  long-text type for semantically unbounded content, and choose its capacity
  from the expected maximum size instead of defaulting to the largest type.
- Use a Unicode-capable character set. Choose collation from required
  case-, accent-, and locale-sensitive comparison semantics, the target
  database version, and existing schema compatibility; do not copy collation
  names across database engines.
- Treat Oracle database character set as a database or PDB concern, not a
  per-schema setting. Preserve the existing character-set contract unless a
  separately planned database-level migration is in scope.
- Store money and other exact quantities as fixed-precision decimal. Derive
  precision and scale from domain range, currency units, intermediate
  calculations, and rounding rules; do not use approximate floating types.
- Before changing a column type, length, character set, collation, precision,
  or nullability, assess compatibility, truncation, rewrite and lock cost,
  deployment order, and rollback.

## Index Design

- Design indexes from real query shapes: predicates, joins, sorting,
  pagination, and uniqueness. Inspect existing indexes and query plans; do not
  add an index merely because a column exists.
- Primary keys are the default identity access path. Audit fields such as
  `creator_id`, `created_at`, `updater_id`, `updated_at`, and `deleted_at` do
  not automatically require standalone indexes.
- Do not index a low-cardinality column alone by default. Allow it when data
  skew, rare-value access, a partial or specialized index, and an actual query
  plan show material benefit.
- For soft-delete tables, design hot-path indexes around the actual active-row
  predicate and target dialect. Do not rely on a standalone soft-delete flag
  or timestamp index for normal list queries.
- Order composite-index columns from complete query shapes, reusable prefixes,
  equality and range predicates, sorting, and pagination. Do not choose column
  order from cardinality alone.
- Index logical foreign-key columns when joins, parent-deletion checks,
  application-managed cascades, existence checks, or cleanup queries require
  it. Because physical foreign keys are prohibited, create required indexes
  explicitly.
- Enforce business uniqueness with a database unique constraint or unique
  index as well as application validation. Verify null and soft-delete
  semantics for composite uniqueness on the target database.
- Treat index-count limits as review signals, not correctness rules. Require
  measured read benefit and explicit write-amplification and storage analysis
  when a table exceeds the project's normal index budget.
- Avoid redundant indexes, but verify uniqueness, query prefixes, sort
  direction, partial predicates, and included columns before removing one.
- Choose indexing strategies for large text or binary values by dialect,
  value size, selectivity, and query semantics. Consider prefix, full-text,
  expression, hash, or external search instead of applying a blanket B-tree
  rule across database engines.
- For large tables, assess lock duration, online or concurrent index options,
  write amplification, deployment order, and rollback before creating or
  rebuilding an index.

## Relationships And Referential Integrity

- For all new schemas and migrations, use logical foreign keys exclusively:
  store the referenced identifier without database-enforced `FOREIGN KEY`
  constraints, ORM-generated foreign-key constraints, or database cascades.
  Do not introduce physical foreign keys.
- The application layer owns referential-integrity validation, concurrency
  control, cascade semantics, and orphan-data governance for every logical
  relationship.
- Do not remove or alter existing physical foreign keys merely to conform to
  this rule. First assess data quality, dependent queries and services,
  migration order, rollback, and compatibility impact.
- Keep logical foreign-key columns compatible with the referenced key's type,
  size, encoding, and identifier semantics. Document the target entity or
  table, column, ownership boundary, cardinality, and delete/update behavior.
- Enforce reference validity in every write path, including APIs, jobs,
  imports, bulk operations, and repair scripts. Protect race-prone checks with
  a transaction and locking or a documented idempotent consistency workflow.
- Implement restrict, soft-delete, cascade, or orphan-retention behavior in
  the owning application workflow. Account for retries, partial failure, and
  idempotency; never rely on implicit database cascades.
- Test missing references and delete/update races on critical paths. For
  important or cross-service relationships, provide bounded, observable
  orphan detection and a safe reconciliation or repair path.

## Migrations And Backfills

- Call out blast radius, compatibility, lock duration, backfill strategy,
  rollback path, and deployment order for schema or data changes.
- Prefer additive, backward-compatible migrations before code starts
  depending on new columns, tables, indexes, or constraints.
- Avoid destructive schema changes in the same deployment as code that stops
  using the old shape unless an explicit compatibility plan exists.
- For large tables, backfill in bounded batches and make the operation
  resumable or idempotent where practical.
- Treat `NOT NULL`, default values, index creation, and column rewrites on
  large tables as potential lock or rewrite risks; verify behavior on the
  target database version before implementation.
