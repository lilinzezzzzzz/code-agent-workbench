---
trigger: model_decision
description: Load for persisted models, database schema, DDL, columns, denormalization, redundant fields, indexes, relationships, constraints, migrations, backfills, or data compatibility.
---
# Database Schema And Migration Rules

Use these rules for persisted structure and data evolution. Establish the
database engine and version, table size and traffic, ownership boundaries,
deployment order, external readers, and rollback expectations first.

## Fields And Constraints

- Model domain invariants explicitly with appropriate types, nullability,
  defaults, checks, and uniqueness. Keep application validation aligned with
  the persisted contract.
- Choose string length, text capacity, binary storage, character set, and
  collation from real value bounds and comparison semantics. Do not copy
  dialect-specific types or collation names across engines.
- Store money and other exact quantities as fixed-precision decimal. Derive
  precision, scale, units, intermediate range, and rounding from the domain;
  do not use approximate floats.
- Define time zone, precision, and clock semantics for timestamps; distinguish
  business time from creation/update audit time.
- Before changing type, length, encoding, collation, precision, default, or
  nullability, assess old and new readers, truncation, rewrite and lock cost,
  replication, deployment order, and rollback.

## Denormalization And Redundant Fields

- Add necessary redundant fields or dedicated read models when they remove
  runtime joins from important read paths and the read benefit justifies the
  additional write, storage, and consistency cost.
- Define one authoritative source for every redundant value. Document its
  provenance, refresh trigger, consistency window, and behavior when the source
  changes or is deleted; do not let multiple copies become independently
  writable sources of truth.
- Keep redundant values synchronized in the same transaction when they share a
  local atomic boundary. Otherwise use an observable, retryable, idempotent
  propagation workflow with outbox/event, checkpoint, or reconciliation as
  appropriate.
- Prefer the smallest stable fields needed by the read contract instead of
  copying an entire related entity. Reassess high-churn, sensitive, large, or
  frequently corrected data because duplication increases update fan-out and
  exposure.
- Provide bounded backfill, drift detection, repair, and rollback for new or
  changed redundant fields. Test source updates, deletes, retries, partial
  propagation, and stale-read behavior.

## Indexes

- Design indexes from complete query shapes: equality and range predicates,
  lookups, ordering, pagination, uniqueness, and active-row filters. Inspect
  existing indexes and representative query plans before adding one.
- Do not index every logical-reference, audit, status, boolean, or soft-delete
  column mechanically. Add an index when lookups, integrity checks, rare-value
  access, cleanup, ordering, or an actual hot path justifies its read benefit.
- Order composite columns from reusable prefixes and real predicates, not
  cardinality folklore. Include a stable tie-breaker where the index supports
  ordered pagination.
- Verify uniqueness, column order, sort direction, included columns,
  expressions, partial predicates, and engine behavior before calling an index
  redundant or removing it.
- For large text/binary or specialized search, choose a dialect-appropriate
  prefix, full-text, expression, hash, or external index rather than assuming a
  universal B-tree strategy.
- Account for write amplification, storage, cache pressure, build time, lock
  behavior, online/concurrent options, replication lag, and rollback on large
  or busy tables.

## Relationships And Referential Integrity

- Use logical references for every newly introduced relationship, reference
  column, schema, or migration, regardless of ownership or datastore boundary.
  Do not add physical `FOREIGN KEY` constraints, ORM-generated foreign-key
  constraints, or database cascades for new relationships.
- Keep each logical reference aligned with the target identifier's type, size,
  encoding, and semantics. Document the target entity and field, ownership,
  cardinality, and update/delete lifecycle.
- The application layer owns referential-integrity validation, concurrency
  control, restrict or cascade behavior, and orphan-data governance for new
  logical relationships.
- Validate logical references in every write path including APIs, jobs,
  imports, bulk operations, migrations, and repair scripts. Protect race-prone
  checks with an atomic operation, lock, transaction, or observable idempotent
  workflow rather than an application pre-check alone.
- Define restrict, soft-delete, cascade, or orphan-retention behavior at the
  application ownership layer. Provide bounded orphan detection and a safe
  reconciliation path on important relationships.
- Add relationship indexes only for demonstrated lookup, lifecycle, cleanup,
  integrity, or reconciliation paths. Test missing references and concurrent
  delete/update behavior where the contract is critical.
- Treat existing physical foreign keys as compatibility surfaces. Do not remove,
  replace, or extend them outside an explicit migration; first assess existing
  data, dependent readers and writers, lock impact, deployment order, rollback,
  and compatibility.

## Migrations And Backfills

- Prefer an expand-migrate-contract sequence: add backward-compatible shape,
  deploy tolerant readers/writers, backfill, verify, enforce the new invariant,
  then remove the old shape only after all consumers have moved.
- Separate schema deployment from application dependency when mixed-version
  instances or rollback can occur. Make old code tolerate additive schema and
  new code tolerate incomplete backfill where necessary.
- Treat `NOT NULL`, defaults, unique constraints, index builds, type changes,
  column rewrites, and table rebuilds as potential lock, rewrite, replication,
  and outage risks. Verify behavior on the exact engine/version.
- Run large backfills in bounded, resumable, observable, and idempotent batches.
  Define ordering, checkpointing, throttling, retry, concurrent-write handling,
  validation queries, and completion criteria.
- Do not combine destructive schema removal with the first deployment that
  stops using it. State rollback limits explicitly when data transformation is
  lossy or dual-write cannot be reversed.
- Review generated migration SQL and downgrade/rollback behavior. Test on
  representative data or a safe rehearsal environment when risk warrants it.
