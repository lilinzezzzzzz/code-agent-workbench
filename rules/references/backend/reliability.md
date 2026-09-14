---
trigger: model_decision
description: Load for services, APIs, workers, auth, validation, configuration, external clients, errors, retries, timeouts, idempotency, observability, or security-sensitive behavior.
---
# Backend Reliability And Security Rules

Use these rules at service, worker, message, and external-integration
boundaries. Derive reliability behavior from the operation's contract and
failure modes.

## Boundaries And Validation

- Use explicit request, response, message, config, and persistence models at
  important boundaries. Validate shape, size, range, encoding, identity, and
  state preconditions before executing side effects.
- Treat client input, headers, uploaded content, queue messages, database data,
  and upstream responses as untrusted at their ownership boundary. Prevent
  injection, path traversal, SSRF, unsafe deserialization, and confused-deputy
  behavior with project-standard controls.
- Keep domain decisions outside routers, controllers, consumers, and framework
  glue when practical. Reuse project helpers for parsing, dependency injection,
  config, error envelopes, logging, metrics, and tracing.
- Preserve API, event, persisted-data, and SDK contracts unless rollout,
  compatibility, and rollback are explicitly part of the task.

## Failure And Distributed Operations

- Classify expected domain failures, invalid input, dependency failures,
  cancellation, and unexpected defects. Do not swallow errors, turn unknown
  failures into success, or hide partial completion.
- Use stable programmatic error codes when clients branch on failure. Keep
  internal details and sensitive values out of public error messages.
- Set timeouts from an end-to-end budget and propagate deadlines and
  cancellation. Avoid independent timeout layers whose combined behavior is
  longer than the caller's budget.
- Retry only transient failures, with bounded attempts, backoff and jitter when
  appropriate. Respect server retry signals and do not multiply retries across
  layers without a budget.
- Make repeated writes safe with an idempotency key, uniqueness or version
  guard, transactional outbox/inbox, deduplication record, or a documented
  equivalent. Define behavior for a duplicate request still in progress.
- For workflows spanning systems, design for partial failure and recovery.
  Do not imply atomicity that the underlying transaction boundary cannot
  provide.
- Bound concurrency, queues, payload size, and memory use. Preserve graceful
  shutdown: stop intake, propagate cancellation, finish or safely requeue
  owned work, and release resources.

## Authorization And Data Protection

- Authenticate the caller and authorize the action against the actual target
  resource and tenant. Default-deny when policy is missing or ambiguous.
- Use least-privilege credentials and secret stores. Never add tokens, private
  keys, cookies, or live credentials to source, logs, fixtures, prompts, or
  command output.
- Minimize sensitive-data collection and exposure. Redact logs and traces;
  avoid full payload logging unless an approved, bounded redaction path exists.
- Validate redirect destinations, webhook targets, file paths, archive
  contents, and outbound URLs before use.

## Observability And Operations

- Emit enough structured context to connect a failure to an operation,
  dependency, tenant-safe identifier, attempt, and latency without exposing
  sensitive content.
- Use metrics and traces for retries, timeouts, queue lag, saturation, partial
  failure, and dependency health when they are operationally material.
- Preserve audit events for privileged or externally visible state changes.
  Ensure observability failure does not silently change business semantics.
