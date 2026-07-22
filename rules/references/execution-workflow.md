---
trigger: model_decision
description: Load for multi-file, ambiguous, risky, data-affecting, API-affecting, externally mutating, blocked, or verification-heavy technical execution.
---
# Execution Workflow Rules

Use this workflow when coordination prevents missed dependencies or unsafe
sequencing. A focused change can proceed directly; a migration or public
contract change needs explicit phases, compatibility, and rollback reasoning.

## Workflow

1. **Understand**: inspect the applicable instructions, source of truth,
   contracts, relevant user diffs, consumers, and representative tests. Resolve
   discoverable facts before asking the user.
2. **Plan when needed**: identify the outcome, affected files, dependencies,
   verification, and any compatibility, migration, security, data, external
   state, or rollback concern. Keep the plan proportional to risk and update it
   when scope changes.
3. **Implement**: make cohesive edits that follow repository patterns. Avoid
   speculative abstractions and broad formatting; keep affected contracts,
   configuration, generated artifacts, tests, and user documentation aligned.
4. **Verify**: run the smallest check capable of falsifying the changed
   behavior, then broaden according to blast radius. Inspect the final diff for
   accidental scope, secrets, generated noise, and compatibility changes.

## Unresolved Decisions And Blockers

- Request direction only when evidence cannot resolve materially different
  public contracts, data models, migration strategies, dependency upgrades, or
  architectures. Continue through low-risk choices resolved by repository
  convention.
- Exhaust safe, in-scope inspection and local alternatives before declaring a
  blocker. Never bypass approval, sandbox, credential, or environment
  boundaries with a workaround.
- If only part of the task is blocked, finish independently verifiable work and
  separate completed results from assumptions or unavailable evidence.
