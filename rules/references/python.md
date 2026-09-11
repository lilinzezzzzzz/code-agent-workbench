---
trigger: model_decision
description: Load for Python implementation, review, refactor, packaging, dependencies, typing, frameworks, workers, or tests.
---
# Python Rules

Follow the repository's Python version, environment, dependency, framework,
typing, and test conventions. For greenfield work with no established stack,
prefer Python 3.11+, `uv`, `pyproject.toml`, Ruff for linting and formatting,
and pytest. Choose frameworks and libraries according to actual needs:
prefer FastAPI, Pydantic v2, SQLAlchemy 2.x, and Alembic for applicable service
and persistence work; apply the async preferences below in projects that
support async coroutines.

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

- Default to meaningful, precise type annotations in new or materially changed
  code, covering function and method signatures and data-model fields. Annotate
  other attributes and local variables when this clarifies intent beyond type
  inference; omit redundant annotations. Specify container element and key/value
  types when known.
- Use `Any` deliberately for dynamic values or when a more precise type adds
  little value, not merely to fill annotation slots. Validate or narrow it when
  runtime correctness, security, persistence, or a public contract depends on
  the value.
- For nullable annotations in Python 3.10+ code, write `T | None`. Do not
  introduce `typing.Optional`, `Optional[T]`, or `Union[T, None]`; preserve
  them only when required by an established Python <3.10 compatibility
  constraint or when an out-of-scope legacy file must remain stylistically
  consistent.
- Use built-in generics. For container annotations, choose the weakest
  `collections.abc` contract that supports every operation the code requires:
  use `Iterable[T]` when only iteration is required, `Sized` for length only,
  `Container[T]` for membership checks only, and `Collection[T]` for iteration,
  length, and membership checks. Use `Sequence[T]` for indexed sequence access,
  `Mapping[K, V]` for key-based reads, and `Set[T]` for set semantics and
  operations. When mutation is required, consider `MutableSequence[T]`,
  `MutableMapping[K, V]`, or `MutableSet[T]` before concrete containers. Use
  `list[T]`, `dict[K, V]`, or `set[T]` when concrete-container behavior or
  ownership of that concrete type is part of the contract. See the
  [collection ABC definitions](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes).
- On Python 3.9+, import collection ABCs such as `Iterable`, `Sequence`,
  `Mapping`, and `Callable` from `collections.abc`, not their deprecated
  `typing` aliases. Use `typing` for constructs it owns, such as `Any`,
  `Literal`, `Protocol`, and `TypedDict`; preserve an established older-version
  compatibility requirement.
- Do not annotate a value as `Iterable[T]` when the implementation requires
  repeated traversal, `len()`, indexing, or materialized storage; choose the
  corresponding stronger interface or explicitly materialize it.
- For generator functions decorated with `@contextmanager`, annotate the
  return type as `Generator[T, None, None]`; for `@asynccontextmanager`, use
  `AsyncGenerator[T, None]`. Import these types from `collections.abc` on
  Python 3.9+. Do not use `Iterator[T]` or `AsyncIterator[T]` for these
  decorated functions. Spell out the type parameters to support Python 3.11
  and 3.12, where the trailing parameters have no defaults.
  The Iterator-based overloads are deprecated in
  [typeshed](https://github.com/python/typeshed/blob/main/stdlib/contextlib.pyi);
  this is a typing deprecation, not a Python runtime prohibition.
- Distinguish generator implementations from context-manager factories:
  ordinary functions returning an existing context manager should use
  `AbstractContextManager[T]` or `AbstractAsyncContextManager[T]` from
  `contextlib`. Keep `Iterator[T]` and `AsyncIterator[T]` for ordinary
  iteration contracts where appropriate; do not replace them indiscriminately.
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
  greenfield work, prefer Ruff for linting and formatting. Follow the project's
  type-checker configuration for typing validation; Ruff does not replace a
  type checker. Do not silence diagnostics without a narrow, documented reason.
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
- In projects that support async coroutines, prefer AnyIO for structured
  concurrency and task groups, HTTPX for HTTP clients, and
  `anyio.to_thread.run_sync` for unavoidable blocking I/O in async paths.
  Apply this preference to new or materially changed code while preserving
  compatibility and keeping unrelated migrations out of scope. Propagate
  cancellation and bound concurrency and resource use.
- Cancelling a task waiting for a worker thread does not stop the thread.
  AnyIO shields that wait from cancellation by default; `abandon_on_cancel=True`
  allows the waiting task to be cancelled while the thread continues running.
  For blocking operations with external side effects, define underlying I/O
  timeouts, cooperative cancellation where supported, and resource ownership
  through completion. See [AnyIO's thread cancellation behavior](https://anyio.readthedocs.io/en/stable/threads.html#running-a-function-in-a-worker-thread).

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
- Select checks and stopping conditions according to `verification.md`, using
  targeted tests and the configured formatter, linter, or type checker as
  applicable. In a standard `uv` setup, use the corresponding `uv run ...`
  commands.
