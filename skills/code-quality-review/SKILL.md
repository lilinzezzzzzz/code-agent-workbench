---
name: code-quality-review
description: Use for focused code-quality review or a lightweight development closeout limited to code quality (代码质量检查、代码质量收尾、代码整理). Covers selected code, a supplied diff, or all current development changes. Assess naming, readability, complexity, abstraction, and duplication. Give actionable suggestions or make the smallest behavior-preserving edits when cleanup is requested.
---

# Code Quality Review

Reduce the effort needed to understand or change code. Treat correctness, observable behavior, and interface compatibility as constraints.

## Scope and authorization

- Start from the code, files, or diff the user identifies. For current development changes, use the scope established in the conversation or inspect the relevant local diff. Read adjacent code, callers, and tests when they affect a conclusion. Preserve unrelated user changes.
- Review, check, and suggestion requests authorize inspection and a report. Requests to clean up the code or apply improvements authorize local edits within the selected scope.
- Choose review depth from the requested outcome. A code-quality closeout can cover the entire current change using this workflow and the relevant local diff. The dedicated `code-changes-review` workflow is separately invoked for a full Git-snapshot review with its own comparison rules.

## Review and cleanup

1. Establish what the code does and which contracts, callers, and edge cases constrain an improvement. Use the [shared code quality checklist](../_shared/code-quality-review-checklist.md) for the relevant aspects of the change.
2. Identify the cost to the reader. Cite the code location and show what the reader would have to infer, which layers or hidden state they would have to trace, or which sites would need to change together. Tie the expected improvement to that concrete cost. Require evidence beyond style preferences, line counts, or speculative reuse. Surface material correctness or compatibility concerns separately from cleanup suggestions.
3. Choose the smallest useful adjustment. First look for confirmed unused code, redundant decisions, pure forwarding, or state that can be derived. Consider adding a helper, flag, or abstraction when it clarifies a responsibility or enforces a contract. Check callers, dynamic registration, failure paths, and side effects as relevant before removing or merging code.
4. Apply and verify authorized edits. Make the smallest safe adjustment and inspect the final diff. Use the smallest practical check that could catch a changed result, error, or side effect. Prefer an existing behavior test or a direct check through the relevant entry point when runtime evidence matters. Keep a candidate as a suggestion if equivalence remains uncertain. Handle behavior fixes only when the user has requested them.

## Report

- Review requests get prioritized findings with a code location, concrete maintenance cost, and an actionable change. Give a short example when it makes the change clearer.
- Cleanup requests get a summary of the edits, their benefit, what behavior was checked and with what result, and material verification gaps. Flag a larger improvement only when the evidence shows a meaningful trade-off to consider.
- If the current implementation is clear enough and available changes offer little benefit, say so and give the reason.
