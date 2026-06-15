---
trigger: model_decision
description: Load for creating, changing, or reviewing HTTP endpoint paths, Router definitions, HTTP methods, resource naming, command actions, or API route contracts.
---
# API Route Design Rules

Use these rules when work creates, changes, or reviews HTTP routes. The default
model is resource-oriented GET reads and command-oriented POST writes because
the target repositories primarily use POST for write operations.

## Core Model

- Use noun-based, resource-oriented paths for GET reads.
- Use an explicit action segment at the end of every POST write path, including
  ordinary resource creation.
- Prefer precise resource and command names over mechanically imitating REST.
- Follow more specific project conventions when they exist. Do not rename an
  existing public route solely for style without a compatibility or deprecation
  plan.

## GET Reads

- Let GET express the read operation. Avoid redundant path actions such as
  `get`, `list`, or `query`.
- Name the resource or read model clearly; change the resource name only when
  the query target would otherwise be ambiguous.
- Use path parameters for resource identity and query parameters for filtering,
  sorting, pagination, and optional projections.
- Prefer paths such as `GET /orders`, `GET /orders/{order_id}`, and
  `GET /orders/{order_id}/items`.

## POST Writes

- Put the command at the end of the path. Prefer these shapes:
  `POST /resources/<action>`, `POST /resources/{resource_id}/<action>`, and
  `POST /resources/<batch-action>`.
- Use `create` to create a new resource. A conflicting stable identity should
  normally fail rather than silently update an existing resource.
- Use `replace` for PUT-style full replacement and `update` for PATCH-style
  partial updates.
- Use `upsert` only when a stable unique key determines whether the command
  creates or updates the resource. Do not use it as a generic synonym for
  `create` or `update`.
- Use `delete` for actual resource deletion. Use `add` and `remove` only for
  relationship or membership changes, not resource creation or deletion.
- Prefer a precise domain action such as `cancel`, `archive`, `approve`,
  `publish`, `activate`, or `revoke` when it describes the state transition
  better than a CRUD action.
- Avoid ambiguous actions such as `save`, `modify`, `change`, `handle`,
  `operate`, or a generic `execute` action with the real command hidden in the
  request body or query string.

Recommended examples:

```text
POST /orders/create
POST /orders/{order_id}/update
POST /orders/{order_id}/cancel
POST /orders/batch-archive
POST /groups/{group_id}/members/add
POST /groups/{group_id}/members/{member_id}/remove
```

Avoid inconsistent shapes such as `POST /create-order`,
`POST /orders/update/{order_id}`, or `POST /execute?action=cancel`.

## Command Contracts

- Define each command's request and response schema, authorization, validation,
  preconditions, state transition, side effects, and stable error behavior.
- Document whether the command is idempotent, whether clients may retry it, and
  how duplicate requests are detected. POST does not make an otherwise
  idempotent command non-idempotent.
- Protect non-idempotent or externally visible side effects with an
  idempotency key, stable business key, uniqueness constraint, or another
  project-standard duplicate guard when retries are possible.
- State whether completion is synchronous or asynchronous. For asynchronous
  commands, define the job or operation resource returned to the caller.
- Keep OpenAPI, SDKs, tests, permissions, metrics, and audit events aligned when
  a route or command contract changes.

## Compatibility

- Treat path, method, request/response schema, error behavior, and idempotency
  as API contract surfaces.
- For an existing route, preserve compatibility or provide an explicit
  migration and deprecation plan. Adding an action segment is not automatically
  a backward-compatible change.
