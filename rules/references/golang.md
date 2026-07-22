---
trigger: model_decision
description: Load for Go implementation, review, refactor, modules, dependencies, package APIs, context, concurrency, tests, or standard tooling.
---
# Go Rules

Use these rules for Go work. The repository's Go version, module layout, build
tags, code generation, tools, and conventions are authoritative.

## Tooling And Modules

- Do not upgrade the `go` or `toolchain` directive or broad dependency sets
  unless the task requires it. Prefer the standard library and existing
  dependencies; assess maintenance, license, security, and transitive cost
  before adding one.
- Use Go commands such as `go get`, `go mod edit`, and `go mod tidy` for module
  metadata. Run `go mod tidy` only when imports, dependencies, or tool metadata
  changed, then inspect `go.mod` and `go.sum` for unrelated churn.
- Never commit temporary local `replace` directives, workspace paths, proxy
  overrides, or credentials. Preserve intentional repository-owned replaces.
- Format changed files with `gofmt` and use the repository's established
  import, lint, generation, and test commands.

## Packages, APIs, And Ownership

- Keep packages cohesive and acyclic. Prefer domain names over vague `util`,
  `common`, or `helpers`; place narrow helpers near their consumer.
- Prefer simple functions and concrete types. Define small interfaces at the
  consuming boundary when multiple implementations or a focused test seam is
  real; do not create one mechanically for each concrete type.
- Make the zero value useful when practical. Constructors should establish
  invariants or dependencies, not merely mirror a struct literal.
- Use pointer receivers for mutation, identity, large values, or types with
  synchronization primitives; use value receivers for small immutable values
  and keep the method set consistent.
- Never copy a value after use when it contains a mutex, `sync.Once`, atomic
  value, or another no-copy resource. Make slice, map, buffer, and pointer
  ownership explicit; copy mutable data when retention or encapsulation
  requires it.
- Use generics for demonstrated type-safe reuse, not to abstract a single call
  site. Keep constraints minimal.
- Avoid mutable package-level state and hidden `init` side effects. Use `init`
  only when intrinsic to the package and testable.

## Errors And Control Flow

- Handle every meaningful error. Discard with `_` only when failure is
  impossible by contract or deliberately irrelevant and the reason is clear.
- Add operation context and preserve causes with `%w`; branch with `errors.Is`
  and `errors.As`, not string matching.
- Use stable sentinel or typed errors only when callers need programmatic
  handling. Keep error strings lowercase and avoid logging and returning the
  same error from layers that do not own the operational log boundary.
- Reserve `panic` for unrecoverable programmer or initialization invariants.
  Expected input, dependency, I/O, and business failures return errors.
- Keep the successful path shallow with early returns; do not sacrifice
  cleanup or state-transition clarity merely to reduce indentation.

## Context, Resources, And Concurrency

- Pass `context.Context` first as `ctx` for I/O or blocking operations. Do not
  store it in structs, pass `nil`, or replace caller context with
  `context.Background` inside the call path.
- Propagate deadlines and cancellation. Call every created cancel function and
  register cleanup only after successful resource acquisition.
- Every goroutine needs an owner, a bounded creation path, and a termination or
  cancellation condition. Wait for started work unless detachment is an
  intentional lifecycle contract.
- The sending owner normally closes a channel. Use channels for ownership
  transfer or coordination and mutexes/atomics for shared memory when clearer;
  neither model is universally preferred.
- Protect shared state and preserve error propagation across concurrent work.
  Avoid sleep-based synchronization, leaked timers, unbounded fan-out, and
  blocking sends with no cancellation path.

## Documentation And Verification

- Document exported contracts, ownership, invariants, concurrency, and
  surprising behavior using repository convention. When no prose-language
  convention exists, use Chinese while keeping identifiers and established
  terms in English.
- Use the standard `testing` package and existing helpers. Prefer table-driven
  tests only when they improve case clarity, and keep tests deterministic and
  parallel-safe.
- Run targeted package tests first, then `go test ./...` and `go vet ./...`
  when blast radius warrants it. Use `go test -race ./...` for concurrency or
  shared-state changes when supported, and the repository vulnerability scan
  for dependency or security-sensitive changes when available.
