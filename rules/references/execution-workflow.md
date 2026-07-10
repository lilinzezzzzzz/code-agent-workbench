---
trigger: model_decision
description: Load for multi-file, ambiguous, risky, data-affecting, API-affecting, externally mutating, blocked, or verification-heavy technical execution.
---
# Execution Workflow Rules

Use this workflow when a task needs coordination beyond a trivial edit. Scale
the ceremony to risk: a focused two-file fix needs a short plan; a migration or
public-contract change needs explicit sequencing and rollback reasoning.

## Workflow

1. **Classify the request**: distinguish explanation, diagnosis, review,
   implementation, Git/history work, and external mutation. Do not broaden the
   user's authorization while trying to complete the task.
2. **Understand**: read the applicable instructions, source of truth,
   contracts, user diffs, consumers, and representative tests. Resolve factual
   questions locally before asking the user.
3. **Plan**: state the outcome, files to change, one-line intent per file, and
   any compatibility, migration, security, data, external-state, or rollback
   concern. Keep one step active at a time and update the plan if scope changes.
4. **Implement**: make cohesive, reviewable edits that follow repository
   patterns. Preserve unrelated work; avoid speculative abstractions and broad
   formatting. Sync required contracts and generated artifacts.
5. **Verify**: run the smallest check that can falsify the changed behavior,
   then broaden based on blast radius. Inspect the final diff for accidental
   scope, secrets, generated noise, and compatibility changes.
6. **Report**: lead with the result, list changed files and observed checks,
   state what was not verified, and identify remaining operational or policy
   risk without restating the full process.

## Decision Gates

Pause for user direction when the next necessary action would:

- Destroy or irreversibly transform user data or uncommitted work.
- Mutate production, an external service, a mailbox, a remote repository, or a
  public deployment beyond the user's explicit request.
- Expose or replace credentials, incur material cost, change access control,
  or weaken a security boundary.
- Choose between materially different public contracts, data models,
  migration strategies, dependency upgrades, or architectures without enough
  repository evidence.

Do not pause for low-risk naming, formatting, or implementation choices that
repository conventions resolve. Choose the conservative option and continue.

## Blockers And Recovery

- Exhaust safe, in-scope inspection and local alternatives before declaring a
  blocker.
- Never bypass approval, sandbox, credential, or environment boundaries with a
  workaround. Report the exact failed command or missing prerequisite and the
  smallest practical next action.
- If only part of the task is blocked, finish independently verifiable work
  and clearly separate completed results from unverified assumptions.
