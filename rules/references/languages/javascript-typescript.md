# JavaScript And TypeScript Rules

Use these rules for JavaScript and TypeScript in browsers, server runtimes,
build tools, and scripts. Browser UI concerns belong to `frontend/web.md`;
server-only or script work does not load that reference automatically.

## Project And Tooling

- Establish the runtime, supported versions, package manager, workspace layout,
  module system, and existing build, lint, type-check, and test commands from
  repository configuration. Preserve the lockfile and use its owning package
  manager; do not create a competing lockfile or mix installation tools.
- When a project requires Node.js and has no established version management
  scheme, prefer nvm for local development where the platform and shell support
  it. When adopting nvm, declare the version in a project-level `.nvmrc`. Do
  not introduce Node.js, nvm, or `.nvmrc` into projects that do not require
  Node.js. See the [nvm project version documentation](https://github.com/nvm-sh/nvm#nvmrc).
- Before dependency installation, builds, or tests that rely on Node.js, verify
  the version in the effective execution environment and activate the required
  version if necessary. Preserve existing version managers and CI/container
  version configuration; do not migrate tooling or upgrade Node.js solely to
  satisfy the nvm preference. If nvm is unavailable or unsuitable, use a
  project-compatible mechanism or an already compliant runtime; if the required
  version cannot be provided, report that prerequisite rather than forcing
  tool installation or shell changes merely to use nvm. Inspect conflicting
  version declarations and make the conflict explicit before choosing a version.
- Follow existing language, formatter, compiler, and lint conventions. Do not
  migrate JavaScript to TypeScript, change ESM/CommonJS boundaries, upgrade
  broad dependency sets, or weaken checks to finish a local task. In a new
  project, select settings for the actual runtime and scope.
- Prefer platform capabilities and existing dependencies. Add packages for a
  concrete need, considering runtime support, maintenance, security, transitive
  dependencies, and browser bundle cost where applicable. Update dependency
  metadata with the project package manager and inspect its diff.
- Respect package exports and server/browser boundaries. Keep server-only
  implementations, secrets, and browser-incompatible runtime dependencies out
  of client bundles. Framework-supported imports that compile to remote-call
  references are allowed; for these imports, verify the emitted client
  artifacts and server execution boundary using the framework build and its
  documented semantics. See the
  [React Server Function import example](https://react.dev/reference/rsc/server-functions#importing-a-server-function-into-a-client-component).
  Avoid surprising I/O and mutable global state during module initialization.

## Types And Data Boundaries

- Use types to describe valid states and public contracts. Prefer simple unions
  and explicit narrowing over complex generic machinery; use discriminated
  unions when they make state transitions safer and clearer.
- Treat untrusted external values as unknown until parsed or validated at the
  owning boundary. Annotations, assertions, and generated client types do not
  validate network responses, stored data, environment values, or user input
  at runtime. Reuse existing validators rather than adding a schema library or
  repeatedly validating trusted internal values without a reason.
- Avoid introducing `any`, non-null assertions, broad casts, or suppression
  comments to hide errors. Narrow nullable values and handle missing branches.
  A necessary interop exception should be narrow, justified, and contained at
  its boundary rather than spreading unchecked types throughout the call path.
- Preserve distinctions among absent, `undefined`, `null`, empty, zero, and
  false according to the contract. Do not reject valid values through truthiness
  checks or silently change omitted fields into explicit updates.
- Keep serialization explicit where it matters: dates and time zones, large
  identifiers beyond safe integer precision, decimal values, and values JSON
  cannot represent. Preserve the wire contract rather than silently coercing
  values to make a type fit.

## Async Work, Errors, And Ownership

- Await or return promises when their result or failure belongs to the caller.
  Intentional background work needs an owner and rejection handling; avoid
  floating promises and async callbacks passed to APIs that ignore promises.
- Handle expected failures at the layer that can recover or present them.
  Preserve error causes and distinguish cancellation from operational failure;
  do not turn a failed operation into an empty successful result.
- Give timers, listeners, subscriptions, streams, and requests a lifecycle
  owner and cleanup path. Propagate cancellation when supported. Cancelling a
  client request does not prove the server stopped or rolled back a write.
- Choose sequential or concurrent execution from dependencies and side
  effects. Bound fan-out for large inputs; promise aggregation does not by
  itself cancel sibling work or make multiple writes atomic.
- Keep mutation and identity ownership clear. Avoid mutating shared inputs or
  framework-owned state; copy at necessary ownership boundaries rather than
  deep-cloning every value or retaining stale mutable references.

## Verification And Documentation

- Follow `workflow/verification.md` and repository commands. Type-checking,
  transpilation, bundling, and runtime tests establish different properties;
  do not claim one passed merely because another did.
- For changed executable behavior, exercise relevant runtime boundaries,
  rejection paths, nullable inputs, and cleanup using existing test tools.
  Do not introduce a new framework or force a full suite for every small edit.
- Check official documentation for version-sensitive runtime, compiler, or
  package behavior. The
  [TypeScript narrowing handbook](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
  explains control-flow narrowing; the
  [type assertion documentation](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions)
  explains why assertions do not add runtime validation.
