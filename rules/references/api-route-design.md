---
trigger: model_decision
description: Load for creating, changing, or reviewing GET/POST HTTP paths, resource naming, command actions, endpoint contracts, OpenAPI, or SDK compatibility.
---
# API Route Design Rules

Use these rules for HTTP endpoint design and review. Only `GET` and `POST` are
supported: GET is resource-oriented and read-only; POST is command-oriented
and handles every write or externally visible action.

## Core Method Model

- First inspect neighboring routes, published specifications, client SDKs, and
  gateway constraints. New routes must follow the GET/POST model; incompatible
  existing routes require an explicit versioned migration rather than another
  style variation.
- Do not introduce `PUT`, `PATCH`, `DELETE`, or another HTTP method. Use GET for
  reads and POST with a precise final action segment for all writes and
  commands.
- Model safe reads as noun-based resources. `GET` must not perform business
  writes or externally visible commands; avoid redundant `get`, `list`, and
  `query` path verbs.
- Put the command at the end of every POST write path, including ordinary
  resource creation, replacement, update, and deletion. Prefer
  `/resources/create`, `/resources/{id}/update`,
  `/resources/{id}/delete`, `/resources/{id}/cancel`, and
  `/resources/batch-archive`.
- Idempotency is defined by the operation contract, not inferred from POST.
- Prefer stable resource nouns and precise domain actions over implementation
  names or generic verbs such as `handle`, `operate`, `process`, `save`, or
  `execute` with the real action hidden in the body.

## Resource And Command Semantics

- Use path parameters for stable identity and hierarchy; use query parameters
  for filtering, sorting, pagination, optional projection, and non-sensitive
  read controls. Do not place credentials or secrets in URLs.
- Use `create` only for resource creation; a conflicting stable identity should
  fail rather than silently update. Use `replace` for full replacement and
  `update` for partial update. Use `upsert` only when a documented stable key
  determines create versus update and both paths share a clear response
  contract.
- Use `add`/`remove` for membership or relationship changes and
  `create`/`delete` for resource lifecycle. Prefer domain actions such as
  `approve`, `publish`, `revoke`, or `cancel` for explicit state transitions.
- Batch endpoints need per-item versus atomic semantics, limits, partial
  failure behavior, ordering expectations, and retry behavior.
- Asynchronous commands should return or identify an operation/job resource
  whose state and failure can be queried. Do not imply synchronous completion
  when work merely entered a queue.

## Contract Checklist

Define and keep aligned:

- Request and response schemas, content types, status codes, validation, and
  stable error codes or envelopes.
- Authentication, authorization on the target resource, tenant context,
  preconditions, state transitions, side effects, and audit behavior.
- Idempotency and retry semantics. Use an idempotency key, stable business key,
  uniqueness constraint, or another duplicate guard where retries can repeat a
  visible write.
- Pagination bounds and stable ordering for collections; caching and
  conditional-request semantics where relevant.
- OpenAPI, gateway/router registration, generated clients, SDKs, examples,
  permissions, metrics, events, and regression tests.

## Compatibility

Treat method, path, parameter location, schema, status and error behavior,
auth, idempotency, and side effects as public contract surfaces. Existing
routes using methods other than GET/POST are non-compliant but still require an
explicit versioning, deprecation, client rollout, and removal plan; do not
break clients through an unannounced method or path replacement.
