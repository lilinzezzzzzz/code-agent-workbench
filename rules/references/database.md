---
trigger: model_decision
description: Load for database, ORM, SQL, DDL, SQLAlchemy, Alembic, schema, relationships, logical foreign keys, index design, migrations, backfills, pagination, N+1, bulk read/write, persistence, transactions, locking, or data-retention tasks.
---
# Database And Persistence Rules

Use these rules when work touches database access, persisted data models,
schemas, indexes, migrations, DDL, column definitions, backfills,
transactions, pagination, or data-retention behavior.

## Query And Persistence Baseline

- Correctness, compatibility, and data safety take priority over change
  scope and code shape.
- Identify persisted formats, schema contracts, external readers, and
  deployment order before changing storage behavior.
- Prefer explicit, bounded queries. Avoid unbounded `SELECT` in user-facing
  or large-data paths; use cursor pagination and explicit `LIMIT`.
- Do not use deep offset pagination such as MySQL `LIMIT offset, size` or
  SQL `OFFSET ... LIMIT` when `offset > 1000`. Treat it as a large scan/row
  discard risk; switch to cursor/keyset pagination with a stable indexed
  sort key instead.
- Do not add `ORDER BY`, ORM `.order_by()`, default model ordering, or
  relationship ordering unless sorting is required for correctness, stable
  public/API behavior, pagination, top-N/latest/oldest semantics, or
  user-visible ordering.
- When deterministic order is required, make it explicit.
  Do not rely on database natural order; for pagination or `LIMIT`, include a
  stable tie-breaker where needed.
- Batch or bulk by default for reads, writes, updates, and deletes. Avoid
  N+1 query patterns; preload required data before iterating.
- Never introduce, approve, or leave ORM, query, or session calls inside
  `for`/`while` loops, comprehensions, or per-item callbacks.
- Keep transaction boundaries explicit. Avoid long transactions and avoid
  external network I/O inside transactions unless the project already has a
  safe pattern for it.

## Schema Field Conventions

- Do not use unconstrained `VARCHAR` or ORM `String` fields at schema
  boundaries. Use an explicit length for short bounded strings, or use the
  database-native large text type for unbounded content.
- For content/body/markdown/prompt-style long text fields, prefer the
  database large text type instead of a large `VARCHAR`: MySQL `MEDIUMTEXT`,
  PostgreSQL `TEXT`, and Oracle `CLOB`.
- For MySQL, use `utf8mb4` with `utf8mb4_unicode_ci` at the database, table,
  or column level unless an existing schema contract requires a different
  charset or collation.
- For PostgreSQL, use database encoding `UTF8`; choose an explicit
  environment-compatible collation or keep the existing database collation.
  Do not use MySQL collation names in PostgreSQL DDL.
- For Oracle, use `AL32UTF8` as the database character set for new schemas.
  Treat collation as an Oracle `NLS` or supported `COLLATE` setting, not a
  MySQL charset/collation clause.
- Store money and other exact decimal quantities as fixed precision decimal:
  MySQL/PostgreSQL `DECIMAL(19,4)` or `NUMERIC(19,4)`, and Oracle
  `NUMBER(19,4)`. Do not use approximate floating types such as `FLOAT`,
  `DOUBLE`, `REAL`, `BINARY_FLOAT`, or `BINARY_DOUBLE` for money.
- When changing an existing column type, charset, collation, or precision,
  call out storage compatibility, rewrite/lock, data truncation, and rollback
  risks before implementing the migration.

## Index Design

- Design indexes from real query shapes: predicates, joins, sorting,
  pagination, uniqueness, and foreign-key access patterns. Inspect existing
  indexes and query plans before adding a new one; do not add speculative
  indexes just because a column exists.
- Treat `id` primary key indexes as the default identity access path. The
  common audit fields `creator_id`, `created_at`, `updater_id`, `updated_at`,
  and `deleted_at` do not automatically require standalone indexes.
- Low-cardinality fields such as `deleted_at`/`deleted`, boolean flags,
  status enums, and small category enums must not be indexed alone. Combine
  them with higher-cardinality columns or use a partial index when the
  database supports it.
- For soft-delete tables, every hot-path lookup/list index should account
  for the active-row predicate. Prefer PostgreSQL partial indexes such as
  `WHERE deleted_at IS NULL`; for MySQL and Oracle, include `deleted_at` in
  the relevant composite index. Do not rely on a standalone `deleted_at`
  index for normal list queries.
- Build composite indexes to match the leftmost-prefix rule: equality
  predicates first, then range predicates, then ordering or pagination
  columns. Put higher-cardinality equality columns before low-cardinality
  fields unless measured query plans show a better order.
- For cursor pagination and deterministic `ORDER BY`, include the ordering
  columns and a stable tie-breaker such as `id` in the same index when the
  query is hot or table size justifies it.
- For the common SQLAlchemy base fields, a typical owner-scoped active list
  index is MySQL/Oracle `(creator_id, deleted_at, created_at, id)` or
  PostgreSQL `(creator_id, created_at, id) WHERE deleted_at IS NULL`. Adjust
  the order to the actual filters and sort direction.
- Index child-side logical foreign-key columns used in joins, parent deletion
  checks, application-managed cascades, existence checks, or cleanup when
  actual query shapes require it. No physical foreign-key constraint will
  create the needed index; verify the query plan and index explicitly.
- Model uniqueness as a database constraint or unique index, not only as an
  application check. For soft-delete uniqueness, prefer partial unique
  indexes where supported; otherwise verify nullable `deleted_at` semantics
  before using it in a unique composite key.
- Keep a conservative index budget. As a default review threshold, keep each
  table at five or fewer indexes including the primary key; write-heavy or
  read-rare tables should usually stay at three or fewer. Exceed the budget
  only with measured read benefit and an explicit write/storage cost review.
- Avoid redundant indexes. A composite index can often cover its leftmost
  prefix, but verify uniqueness, foreign-key requirements, sort direction,
  partial predicates, and included columns before removing or rejecting a
  separate index.
- Do not create ordinary B-tree indexes on `TEXT`, `BLOB`, `CLOB`, or other
  large object fields. Use a prefix index, full-text/search index,
  expression/hash index, or external search system according to the query
  semantics and database support.
- Keep indexes narrow. Avoid indexing large variable-length fields,
  low-selectivity prefixes, or many projected columns unless a covering index
  is justified by a hot query and supported by the database.
- For large tables, treat index creation as a migration risk. Call out lock
  duration, online/concurrent index options, rollback path, deployment order,
  index length limits, and write amplification before implementation.

## Relationships And Referential Integrity

- For all new schemas and migrations, use logical foreign keys exclusively:
  store the referenced identifier without creating database-enforced
  `FOREIGN KEY` constraints, ORM-generated foreign-key constraints, or
  database cascades. Do not introduce physical foreign keys.
- The application layer owns referential-integrity validation, concurrency
  control, cascade semantics, and orphan-data governance for every logical
  relationship; do not assume the database will enforce them implicitly.
- Do not remove or alter existing physical foreign keys merely to conform to
  this rule. First assess data quality, dependent queries and services,
  migration order, rollback, and compatibility impact.
- Keep each logical foreign-key column compatible with the referenced key's
  type, size, encoding, and identifier semantics. Document the referenced
  table or entity, column, ownership boundary, cardinality, and expected
  delete/update behavior in the schema, model, or migration.
- Enforce referential validity in every write path, including APIs, jobs,
  imports, bulk operations, and repair scripts. Where concurrency can race a
  validation check, use an explicit transaction and locking or a documented
  idempotent consistency workflow instead of assuming an application-side
  pre-check is sufficient.
- Define deletion and referenced-key update semantics explicitly. Implement
  restrict, soft-delete, cascade, or orphan-retention behavior in the owning
  application workflow, and account for retries, partial failure, and
  idempotency; never rely on implicit database cascades.
- Add tests for missing references and delete/update races on critical write
  paths. For important or cross-service relationships, provide bounded,
  observable orphan detection and a safe reconciliation or repair path.

## Migrations And Backfills

- Call out blast radius, compatibility, lock duration, backfill strategy,
  rollback path, and deployment order for schema or data changes.
- Prefer additive, backward-compatible migrations before code starts
  depending on new columns, tables, or constraints.
- Avoid destructive schema changes in the same deployment as code that
  stops using the old shape unless an explicit compatibility plan exists.
- For large tables, backfill in bounded batches and make the operation
  resumable or idempotent where practical.
- Be careful with `NOT NULL`, default values, and column rewrites on large
  tables. Flag lock or rewrite risk before implementation.
- Ask before running data-mutating migrations, broad backfills, or cleanup
  commands against real environments.
