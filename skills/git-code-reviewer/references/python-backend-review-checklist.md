# Python Backend Review Checklist

Use only the sections relevant to the change. This is a thinking aid for Python services and workers, not a template to dump verbatim.

## 1. API Boundary and Validation

- Did request parsing, validation, or coercion semantics change for FastAPI, Starlette, Pydantic, dataclass, or custom transport models?
- Did the change alter omitted-vs-`null`, default, alias, enum, or serialization behavior in a way that breaks existing clients or stored payloads?
- Are status codes, error envelopes, exception handlers, or response models still aligned with the API contract?
- Does the handler now return ORM objects, lazy fields, or partially shaped dicts that may fail serialization or trigger late database access?

## 2. Dependency Injection, Auth, and Tenant Context

- Did dependency wiring, middleware ordering, or request-scoped objects such as auth context, tenant context, DB session, or trace context change?
- Are authn and authz checks preserved on every sensitive path, including background or internal helper paths?
- Could tenant filters, soft-delete filters, or row-level access checks be bypassed by moved or shared query code?

## 3. Service Logic and Error Contracts

- Are domain errors mapped to stable API-facing or job-facing error shapes instead of leaking raw exceptions?
- Do retries, partial failures, or fallback branches change state transitions or produce duplicate side effects?
- Does the change move validation or normalization deeper into the stack and make failures harder to classify or recover from?

## 4. SQLAlchemy, Transactions, and Persistence

- Is the session lifecycle clear, including commit, rollback, flush, and close boundaries?
- Could the change introduce read-modify-write races, duplicate inserts, missing uniqueness checks, or non-idempotent writes under retry?
- Does lazy loading, eager loading, relationship traversal, or serialization create N+1 queries or `DetachedInstanceError`-style failures?
- Does a `for`/`while` loop, comprehension, serializer, or per-item callback
  execute one SQL query per row instead of using a join, `selectinload`,
  `joinedload`, bulk query, or bounded batch?
- Are tenant predicates, soft-delete predicates, and pagination or ordering semantics preserved?
- Does the implementation call `.all()`, `list(...)`, unbounded
  `scalars().all()`, or ORM relationship traversal in a way that loads the
  full result set or object graph into memory?

## 5. Migrations and Data Changes

- Is the Alembic migration safe for mixed-version rollout, or does it require an explicit expand-contract sequence?
- Do nullability changes, column drops, renames, backfills, or default changes have a rollback path and bounded lock duration?
- If data is rewritten, is the backfill idempotent, resumable, and safe under partial failure?
- Were application code, migration scripts, and tests updated together when the persisted schema or enum set changed?

## 6. Async, Background Jobs, and External I/O

- Does async code accidentally call blocking I/O such as sync DB access, filesystem work, or network clients on the event loop?
- Are timeout, retry, cancellation, and deadline semantics explicit for `httpx`, message queues, LLM calls, storage SDKs, or other external dependencies?
- Does synchronous external API or LLM I/O run on a request or worker hot path
  without explicit timeout, concurrency isolation, circuit-breaker/bulkhead, or
  queue/offload configuration?
- Does the code read a whole upload, export, object-store blob, archive, or
  generated file into memory when streaming, chunked reads, or bounded spooling
  would preserve behavior?
- Could a background task or worker run after the request fails or times out and leave the system in an inconsistent state?
- For Celery, RQ, Dramatiq, Arq, or framework-native background tasks, are retries, acknowledgements, duplicate delivery, and task ordering safe for the underlying writes and side effects?
- Are queues, tasks, and scheduled jobs idempotent and deduplicated where retries or duplicate delivery are possible?

## 7. Configuration, Settings, and Runtime Safety

- Did environment-variable parsing, feature flags, defaults, or settings precedence change?
- Could a configuration typo now fail open instead of fail closed?
- Are secrets, tokens, raw prompts, tenant identifiers, or user content exposed in logs, metrics, traces, or exceptions?

## 8. Python-Specific Security Pitfalls

- Does the change introduce unsafe deserialization such as `pickle`, `yaml.load`, or untrusted model loading?
- Are `subprocess`, file paths, URLs, templates, or dynamic imports built from untrusted input without validation?
- Could the new code allow SSRF, path traversal, command injection, template injection, or prompt leakage across trust boundaries?

## 9. Typing and Interface Precision

- Did the change make function signatures, request models, repository interfaces, or settings objects less precise in a way that hides real `None` or shape errors?
- Did the change replace a named or typed internal structure with an opaque positional tuple or loose container at an important boundary, making the contract harder to review or easier to misuse?
- Could the implementation now violate declared types, for example returning `None` where the annotation promises a value, widening to loose dict payloads, or breaking `TypedDict`, Pydantic, or protocol expectations?
- Did helper parameters, fallback branches, or review-scope wrappers become behaviorally dead after the change, indicating obsolete code that should likely be removed?
- If the repository uses `mypy`, `pyright`, or Pylance-strict conventions, would the changed code still satisfy the intended type boundary rather than merely passing at runtime?

## 10. Tests and Verification

- Do tests cover the changed request or response contract, not just internal helpers?
- Is there a failure-path test for validation, authz, external timeouts, partial writes, or duplicate delivery where relevant?
- If persistence behavior changed, is there at least one integration-style verification of transaction boundaries, rollback, or migration compatibility?
- If type-sensitive code changed, is there a targeted type-checking signal or an explicit statement that type compatibility remains unverified?
- If no targeted validation was run, is the review output explicit about what remains unverified?
