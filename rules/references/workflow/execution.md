---
trigger: model_decision
description: Load for multi-file, ambiguous, risky, data-affecting, API-affecting, externally mutating, blocked, or verification-heavy technical execution.
---
# Execution Workflow Rules

Use this workflow when coordination prevents missed dependencies or unsafe
sequencing. A focused change can proceed directly; a migration or public
contract change needs explicit phases, compatibility, and rollback reasoning.
Apply the global agent instructions' authorization and completion boundaries;
planning is not a separate approval gate for already authorized work.

## Workflow

1. **Understand**: inspect the applicable instructions, source of truth,
   contracts, relevant user diffs, consumers, and representative tests. Resolve
   discoverable facts before asking the user.
2. **Plan when needed**: identify the outcome, affected files, dependencies,
   verification, and any compatibility, migration, security, data, external
   state, or rollback concern. Keep the plan proportional to risk and update it
   when scope changes.
3. **Implement when authorized**: for change requests, make cohesive edits
   that follow repository patterns. Avoid speculative abstractions and broad
   formatting; keep affected contracts and supporting artifacts aligned.
   For review, diagnosis, explanation, or planning requests, inspect evidence
   and deliver the requested analysis without entering implementation.
4. **Verify**: run the smallest check capable of falsifying the changed
   behavior, then broaden according to blast radius. Inspect the final diff for
   accidental scope, secrets, generated noise, and compatibility changes.
   Before finalizing, reconcile the result with the user's requested outcomes
   and accepted follow-up requirements. Complete omissions within scope and
   identify anything remaining. Use an explicit checklist only when complexity
   warrants it.

## Tool Failures And Retries

- If an operation times out or returns an ambiguous result, inspect its state
  before retrying. Do not repeat a potentially completed side effect unless
  duplicate execution is prevented or evidence shows it did not occur.
  Continue independent work while resolving the uncertain outcome.
- Retry with a concrete reason to expect a different result, such as corrected
  input, changed state, or a plausibly transient failure. If the same blocker
  persists without new evidence, stop that path, report what would unblock it,
  and continue independent work. These rules do not waive approval requirements.

## Unresolved Decisions And Blockers

- Ask when an unresolved choice materially changes the requested outcome,
  compatibility, data safety, security, cost, or authorized external effects,
  and cannot be resolved from instructions, evidence, repository conventions,
  or a conservative reversible assumption.
- The existence of multiple reasonable implementations is not itself a blocker.
  Do not interrupt for optional preferences. Ask blocking questions promptly
  after relevant inspection, and continue independent authorized work.
- Examine relevant safe, in-scope evidence and viable local alternatives before
  declaring a blocker; follow the retry limits above rather than repeating
  ineffective attempts. Never bypass approval, sandbox, credential, or
  environment boundaries with a workaround.
- If only part of the task is blocked, finish independently verifiable work and
  separate completed results from assumptions or unavailable evidence.
