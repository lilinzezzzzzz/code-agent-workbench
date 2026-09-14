---
trigger: model_decision
description: Load for creating, changing, or reviewing HTTP paths, method conventions, resource naming, command actions, endpoint contracts, OpenAPI, or SDK compatibility.
---
# API Route Design Rules

Use these rules for HTTP endpoint design and review. First establish the
repository's published method and path convention; preserve one coherent API
style instead of imposing a cross-project default.

## Method And Path Model

- Inspect neighboring routes, OpenAPI, gateway constraints, and client SDKs.
  Follow the established convention for compatible additions; changing the
  convention requires an explicit versioned migration.
- In a GET/POST-only system, use GET for read-only resource retrieval and POST
  for every write or externally visible command. Do not add PUT, PATCH, DELETE,
  or another method to that system.
- In a GET/POST-only system, keep GET paths noun-oriented without redundant
  `get`, `list`, or `query` verbs. Put a precise action at the end of every POST
  path, including `/resources/create`, `/resources/{id}/update`,
  `/resources/{id}/delete`, or `/resources/{id}/cancel`.
- In a system using standard REST method semantics, follow its established
  GET/POST/PUT/PATCH/DELETE contract and resource naming. Do not introduce the
  GET/POST command style as an unrequested second convention.
- Prefer stable resource nouns and precise domain actions over implementation
  names or generic verbs such as `handle`, `operate`, `process`, or `execute`.
  Idempotency comes from the operation contract, not the HTTP method alone.

## Resource And Command Semantics

- Use path parameters for stable identity and hierarchy; use query parameters
  for filtering, sorting, pagination, optional projection, and non-sensitive
  read controls. Do not place credentials or secrets in URLs.
- In command-style APIs, use `create` only for resource creation; a conflicting
  stable identity should fail rather than silently update. Use `replace` for
  full replacement, `update` for partial update, and `upsert` only when a
  documented stable key determines both paths and response semantics.
- Use `add`/`remove` for membership or relationship changes and
  `create`/`delete` for resource lifecycle. Prefer domain actions such as
  `approve`, `publish`, `revoke`, or `cancel` for state transitions.
- Batch endpoints need per-item versus atomic semantics, limits, partial
  failure behavior, ordering expectations, and retry behavior.
- Asynchronous commands should return or identify an operation or job resource
  whose state and failure can be queried. Do not imply synchronous completion
  when work merely entered a queue.

## Contract Checklist

Keep aligned:

- Request and response schemas, content types, status codes, validation, and
  stable error codes or envelopes.
- Authentication, authorization on the target resource, tenant context,
  preconditions, state transitions, side effects, and audit behavior.
- Idempotency and retry semantics, with a duplicate guard when retries can
  repeat a visible write.
- Pagination bounds and stable ordering; caching and conditional requests where
  relevant.
- OpenAPI, gateway registration, generated clients, SDKs, examples,
  permissions, metrics, events, and regression tests.

Treat method, path, parameter location, schema, status and error behavior,
authorization, idempotency, and side effects as public contracts. Incompatible
existing routes require versioning, deprecation, client rollout, and removal
planning rather than an unannounced replacement.
