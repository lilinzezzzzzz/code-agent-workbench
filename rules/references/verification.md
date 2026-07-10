---
trigger: model_decision
description: Load for behavior changes, bug fixes, test planning, regression coverage, CI failures, lint, type-checking, artifact validation, or reporting verification claims.
---
# Verification Rules

Verification should produce evidence for the claims made about the change. Run
the smallest meaningful check first, then expand only when the blast radius or
repository convention justifies it.

## Build The Verification Plan

1. State the behavior, contract, or artifact property that could be wrong.
2. Choose the fastest check capable of falsifying it: focused static check,
   targeted unit test, integration test, build, render, migration rehearsal, or
   manual runtime observation.
3. Add broader tests, lint, type-checking, race detection, security scans, or
   end-to-end checks for shared, concurrent, persistence, auth, dependency, or
   cross-service changes.
4. Use repository commands, environments, fixtures, and helpers. Do not add a
   new test framework merely to validate a small change.

## Test Quality

- Bug fixes should reproduce the failure and prove the corrected behavior when
  a practical automated test path exists.
- Cover meaningful success, failure, boundary, and state-transition cases;
  avoid duplicating implementation details in assertions.
- Keep tests deterministic, isolated, and safe to repeat. Control time,
  randomness, concurrency, and external I/O with project-standard mechanisms.
- Mock at ownership or external-system boundaries. Do not mock the behavior
  under test or claim integration coverage from fully mocked collaborators.
- Never run destructive tests against production or shared data. Confirm the
  target environment before migrations, backfills, load tests, or externally
  visible side effects.

## Non-Code Artifacts

- For documentation and agent rules, check frontmatter, headings, internal
  paths, filenames, examples, trigger coverage, and contradictions with the
  source of truth.
- For configuration and schemas, use the owning parser, validator, generator,
  dry-run, or diff command when available; text inspection alone may miss
  semantic errors.
- For generated or visual artifacts, regenerate or render and compare the
  actual output rather than assuming source validity.

## Evidence And Reporting

- Observe exit status and relevant output. A command that did not run to
  completion is not a pass.
- Do not claim coverage unless measured. Do not infer runtime compatibility or
  performance from code inspection alone.
- Report commands with outcomes. If a check was skipped or blocked, state the
  exact command when known, the reason, and the remaining risk.
- Expected failures from a deliberate negative test are evidence only when the
  failure mode and assertion match the intended contract.
