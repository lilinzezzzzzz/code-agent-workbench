---
trigger: model_decision
description: Must be loaded before any Go implementation, review, refactor, module, dependency, test, tooling, context, concurrency, or package API task.
---
# Go Rules

Use these rules for Go implementation, review, refactor, module, dependency,
test, tooling, context, concurrency, or package API work. These are language
and standard-tooling rules; do not infer framework choices from them.

## Baseline And Tooling

- Follow the Go version, module layout, build tags, and commands declared by
  the repository. Do not upgrade the `go` or `toolchain` directive unless the
  task explicitly requires it.
- Prefer the standard library and existing dependencies. Add a third-party
  dependency only when it removes meaningful complexity and its maintenance,
  license, security, and transitive dependency costs are acceptable.
- Format changed Go files with `gofmt`. Preserve the repository's established
  import tooling when it uses `goimports` or another formatter.
- Keep packages cohesive and acyclic. Use short, lowercase package names;
  avoid vague packages such as `util`, `common`, or `helpers` when a domain
  name or placement beside the caller is clearer.
- Avoid mutable package-level state. Use `init` only when initialization is
  intrinsic to the package and the side effect is documented and testable.

## Modules And Dependencies

- Treat `go.mod` and `go.sum` as source-controlled artifacts. Use Go commands
  such as `go get`, `go mod edit`, and `go mod tidy` instead of manually
  constructing module metadata.
- Run `go mod tidy` only when imports, dependencies, module metadata, or tool
  dependencies changed, then inspect both `go.mod` and `go.sum` for unrelated
  upgrades or removals.
- Do not commit temporary local `replace` directives, workspace paths, proxy
  overrides, or private credentials. Preserve intentional repository-owned
  replacements and explain compatibility-sensitive changes.
- Keep dependency upgrades scoped and explicit. Do not combine broad module
  upgrades with an unrelated code change.

## APIs, Types, And Ownership

- Prefer concrete types and simple functions. Add interfaces at the consuming
  boundary when multiple implementations or a focused test seam are needed;
  keep interfaces small and do not create one mechanically for every type.
- Accept interfaces and return concrete types by default, unless an existing
  public contract or multiple interchangeable implementations require a
  different shape.
- Make the zero value useful when practical. Constructors should establish
  invariants or dependencies, not exist only to mirror a struct literal.
- Choose pointer receivers for mutation, identity, large values, or types that
  contain synchronization primitives. Use value receivers for small immutable
  values, and keep the receiver choice consistent across a type's method set.
- Never copy a value after first use when it contains `sync.Mutex`,
  `sync.RWMutex`, `sync.Once`, `atomic` types, or another no-copy resource.
- Make slice, map, buffer, and pointer ownership clear at API boundaries. Copy
  mutable data when the callee must retain it or when callers must not observe
  internal mutation.
- Use generics only for demonstrated type-safe reuse. Keep constraints minimal
  and prefer ordinary functions or interfaces when they express behavior more
  clearly.

## Errors And Control Flow

- Handle every meaningful error. Do not discard errors with `_` unless failure
  is impossible by contract or intentionally irrelevant and the reason is
  documented.
- Add actionable context when propagating errors and preserve the cause with
  `fmt.Errorf("operation: %w", err)`. Use `errors.Is` and `errors.As`; do not
  inspect error strings for control flow.
- Keep error strings lowercase and without trailing punctuation unless they
  begin with a proper noun or acronym. Avoid logging an error and returning it
  from the same layer unless that layer owns the operational log boundary.
- Use sentinel or typed errors only when callers need stable programmatic
  handling. Keep error APIs narrow and avoid exposing implementation details.
- Reserve `panic` for unrecoverable programmer errors or broken initialization
  invariants. Expected input, I/O, dependency, and business failures return
  errors.
- Keep the successful path minimally indented. Handle errors early and avoid
  an `else` after a branch that returns, continues, or breaks.

## Context, Resources, And Concurrency

- Pass `context.Context` as the first parameter named `ctx` for operations that
  cross process boundaries, perform I/O, or may block. Do not store contexts in
  structs, pass `nil`, or replace a caller's context with `context.Background`.
- Propagate cancellation and deadlines through downstream calls. A function
  that creates a cancel function must call it, normally with `defer cancel()`.
- Acquire resources and register cleanup close together. Call `defer` only
  after successful acquisition, and handle cleanup errors when they can affect
  correctness, durability, or protocol completion.
- Every goroutine must have an explicit owner, termination condition, and
  cancellation or completion path. Do not leak goroutines or launch unbounded
  work from loops, handlers, or consumers.
- The sender that owns a channel normally closes it. Do not close a channel
  from a receiver or use channel closure as a substitute for synchronization
  without clear ownership.
- Protect shared state explicitly. Use channels for ownership transfer or
  coordination and mutexes or atomics for shared memory when they are clearer;
  do not force either model as a universal rule.
- Preserve cancellation and error propagation across concurrent work. Use
  bounded concurrency and wait for started work unless detachment is an
  intentional, documented lifecycle decision.

## Documentation And Tests

- Public packages and exported declarations need useful doc comments. Begin an
  exported declaration's comment with its name; use Chinese prose by default
  while preserving identifiers and established technical terms in English.
- Comments explain contracts, ownership, concurrency, invariants, and reasons;
  do not narrate syntax. Keep examples executable when they define intended
  package usage.
- Use the standard `testing` package and the repository's existing helpers.
  Prefer table-driven tests when they make cases easier to add and compare, not
  when they obscure setup or assertions.
- Keep tests deterministic and parallel-safe. Avoid timing-based sleeps;
  coordinate with channels, contexts, clocks, or explicit synchronization.
- Run targeted package tests first, then `go test ./...` from the relevant
  module root. Run `go vet ./...` for behavior changes and
  `go test -race ./...` when concurrency or shared state changed and the
  environment supports it.
- When dependencies or security-sensitive code change, run the repository's
  vulnerability scan or `govulncheck ./...` if available. Do not claim a clean
  result when the tool was unavailable or the scan was not run.
