---
trigger: model_decision
description: Load for Python implementation, review, refactor, packaging, dependencies, typing, frameworks, workers, or tests.
---
# Python Rules

Follow the repository's Python version, environment, dependency, framework,
typing, and test conventions. For greenfield work with no established stack,
prefer Python 3.11+, `uv`, `pyproject.toml`, Ruff-compatible typing, FastAPI,
Pydantic v2, SQLAlchemy 2.x, Alembic, AnyIO, HTTPX, and pytest.

## Environment And Dependencies

- Use the repository's supported Python versions and pinning mechanism. For
  greenfield work, use Python 3.11 or newer and pin it in project configuration.
- Use the repository's environment and dependency tool. When it uses `uv`,
  prefer `uv run ...` over bare `python`, `pip`, `pytest`, `ruff`, or
  type-checker commands.
- In `uv` projects, use `uv sync` to materialize the environment,
  `uv add`/`uv remove` for dependencies, and `uv lock` when only lock metadata
  requires refresh. Inspect `pyproject.toml` and `uv.lock` for unrelated churn.
- Avoid unrelated upgrades. Verify package, API, and version details from
  installed metadata or current primary documentation when they matter.

## Types And Data Models

- Add precise annotations at public and important internal boundaries. `Any`
  is allowed; use it deliberately for dynamic values or when a more precise
  type adds little value. Validate or narrow it when runtime correctness,
  security, persistence, or a public contract depends on the value.
- Use built-in generics and PEP 604 unions such as `X | None`. For container
  annotations, choose the weakest `collections.abc` contract that supports
  every operation the code requires: use `Iterable[T]` for single-pass
  iteration only, `Sequence[T]` when order, `len()`, or index access is
  required, `Mapping[K, V]` for key-based reads, and `Set[T]` for membership
  checks or set operations without ordering. Use concrete `list[T]`,
  `dict[K, V]`, or `set[T]` when mutation, concrete ownership, or
  concrete-container behavior is part of the contract.
- Do not annotate a value as `Iterable[T]` when the implementation requires
  repeated traversal, `len()`, indexing, or materialized storage; choose the
  corresponding stronger interface or explicitly materialize it.
- Use `TypedDict` for a mapping-shaped contract, `dataclass` for a plain data
  carrier, and Pydantic v2 models for validated I/O. Do not use a runtime model
  for a local internal record without validation needs.
- Use `Enum`/`StrEnum` when values need runtime identity, shared behavior,
  validation, or stable wire/persistence semantics. Use `Literal` for narrow
  type-only choices, overloads, and discriminated tags.
- Make optionality, ownership, mutability, units, time zones, and serialization
  behavior explicit at boundaries.
- Narrow every optional value before passing it to a non-optional boundary. If
  several optional variables describe one valid state, guard all values used by
  that state together; do not rely on an earlier assignment or another
  variable's non-null check to narrow them implicitly.
- Prefer an early `return`/`continue` guard such as
  `if path is None or section is None: continue`. When the values must always
  co-exist, model them as one object or a discriminated state instead of
  parallel optional variables.
- Use `assert value is not None` only after an established invariant. Do not
  use `cast`, `# type: ignore`, or a redundant annotation merely to suppress a
  Pylance/type-checker error; correct the control flow or data model instead.

## Design And Imports

- Prefer simple module functions and concrete classes. Introduce a small,
  consumer-owned `Protocol` when multiple implementations or a useful boundary
  test seam exists; use `ABC` only when nominal inheritance or shared
  implementation is required.
- When a concrete class is intentionally a named implementation of a
  `Protocol`, explicitly inherit that `Protocol` when the contract is in a
  neutral dependency layer and doing so does not create a circular dependency.
  This keeps implementation relationships discoverable to readers, IDEs, and
  type checkers. Retain structural conformance when explicit inheritance would
  reverse the intended dependency direction or cross an ownership boundary.
- Keep imports at module level by default. A local import is acceptable for a
  proven circular dependency, optional dependency, startup-cost boundary, or
  framework registration constraint; keep the reason apparent.
- Use the repository's configured formatter, linter, and type checker. For
  greenfield work, prefer Ruff and Pylance-compatible typing; do not silence
  diagnostics without a narrow, documented reason.
- Prefer keyword arguments when they clarify call sites, but preserve public
  call compatibility and conventional positional parameters.

## Errors, Resources, And Async

- Raise built-in exceptions for programming and value-contract errors. Use a
  small domain exception hierarchy only when callers need stable business
  handling; do not use exception strings as programmatic error codes.
- Preserve the cause when translating errors and add context at ownership
  boundaries. Do not catch `Exception` merely to log and continue or return a
  false success.
- Manage files, streams, clients, sessions, transactions, tasks, and temporary
  resources with context managers or explicit lifecycle ownership.
- Use AnyIO structured concurrency and task groups for concurrent async work,
  HTTPX for HTTP clients, and `anyio.to_thread.run_sync` for unavoidable
  blocking I/O. Propagate cancellation and bound concurrency and resource use.

## Frameworks And Persistence

- In FastAPI services, use explicit request/response models, `Depends` for
  dependency injection, and the service's stable error envelope.
- In Pydantic v2 projects, use v2 APIs and validators. Preserve an established
  v1 compatibility requirement unless migration is in scope.
- In SQLAlchemy 2.x projects, use typed models, queries, and session patterns.
  Use the repository's migration framework as the source of truth.
- Keep transport validation, dependency injection, ORM/session ownership, and
  domain logic separated enough that core behavior can be tested without a
  live framework stack.

## Documentation And Verification

- Document public contracts and non-obvious invariants. Comments explain why,
  ownership, and edge behavior rather than narrating syntax. Follow the
  repository's prose language; when none is established, use Chinese for new or
  changed comments.
- Use the repository's test framework; for greenfield work, prefer pytest. Keep
  real domain logic with fakes or mocks only at external I/O and ownership
  boundaries.
- Run targeted tests first, then the configured formatter or linter, type
  checker, and broader test suite according to blast radius. In a standard `uv`
  setup, use the corresponding `uv run ...` commands.
