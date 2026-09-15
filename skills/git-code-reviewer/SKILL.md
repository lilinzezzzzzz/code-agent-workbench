---
name: git-code-reviewer
description: Review a Python backend service's complete current branch against a user-specified base before PR/MR submission, or review its current staged changes. Invoke explicitly with $git-code-reviewer for whole-branch or staged review (检查当前 staged 代码 / 检查暂存区); do not use for unstaged workspace changes, individual commits or arbitrary diffs, localized implementation checks, or debugging.
---

# Code Review

Turn a change set into evidence-backed findings. Prioritize correctness and operational risk over style.

## Scope Gate

- Choose the review mode from the user's request: complete-branch pre-PR/MR review or current staged/index review. A request such as `检查当前 staged 代码` or `检查暂存区` selects staged mode, even when a base was provided earlier. If the intended scope is unclear, ask whether to review the complete branch or staged changes; do not infer it from a nonempty index or a default prompt example.
- Unstaged workspace, individual commit, arbitrary diff, debugging, design-conformance, and localized code-review requests use normal code inspection instead of this workflow.
- Once the selected mode's prerequisites are satisfied, complete the authorized review and report without asking whether to proceed.
- Identify the reviewed snapshot before inspecting content. For branch mode, record the resolved base, merge-base, and HEAD commit SHAs. For staged mode, record HEAD (or its absence) and an index snapshot identifier, such as a tree ID obtained from a temporary copy of the index. Do not stash, stage, or alter the real index merely to identify the snapshot; no worktree is required by default. If identification is unavailable, disclose the reproducibility limitation.

### Complete Branch

- Require a base branch or base ref explicitly provided by the user, including an earlier instruction that remains applicable to this review. If missing, ask `基础分支是什么？`; do not resolve the comparison range, fetch, or begin branch-delta review. Do not infer the base from PR metadata, repository defaults, the current branch, or local context.
- Independent read-only preparation, such as locating repository instructions and inspecting workspace status, may continue while the base is missing.
- After receiving the base, load and follow [../_shared/git-remote-base-resolution.md](../_shared/git-remote-base-resolution.md) for ref resolution and freshness.
- Review the committed branch delta from the merge base through the current `HEAD`. Report relevant staged, unstaged, and untracked workspace changes separately; do not silently include them in the branch artifact.
- Keep evidence tied to the reviewed revision: when workspace changes affect inspected files or validation inputs, use committed content for branch conclusions and state which revision each check actually validates. Do not attribute workspace-only fixes or passing tests to `HEAD`. Preserve user changes; if committed-state validation is unavailable, report that limitation.

### Staged Changes

- Review only the delta from `HEAD` to the index using `git diff --cached`. No user-provided base, remote ref resolution, or fetch is required; do not load the remote-base guidance for this mode. On an unborn branch, review the staged additions against the empty tree.
- If the index has no staged changes, report that and stop; do not expand to the branch or workspace. If it contains unresolved merge entries, report that the staged artifact is not ready for review; do not resolve conflicts or change the index.
- Read staged file content from the index, for example with `git show :path/to/file`, and compare with `HEAD` where relevant. A file can contain both staged and unstaged edits; do not substitute its working-tree content for its staged version. Exclude unstaged and untracked changes from the artifact.
- Inspect relevant callers, tests, and configuration as context, using the index version when available. Tie findings to the staged delta rather than unrelated existing defects. Keep evidence tied to the inspected index state; if it changes during review, recheck affected conclusions before reporting.
- State whether checks validated the staged snapshot or the working tree. Working-tree checks may include unstaged edits or untracked inputs and do not by themselves prove the staged snapshot passes. Preserve user changes and the index; if staged-state validation is unavailable, report that limitation.

## Workflow

### 1. Understand the Change

- Read the diff summary, changed implementation, and relevant runtime path before judging intent.
- Inventory all changed files, including additions, deletions, renames, configuration, and generated artifacts. Assess each file's risk before selecting paths for deeper inspection. Read large or truncated diffs in batches; disclose uninspected portions rather than implying complete coverage. A per-file report is unnecessary.
- Establish intended behavior from applicable repository instructions, contracts, and accepted project decisions. Do not impose a preferred architecture or introduce universal redaction, retry, lock, or fallback requirements without a concrete risk in the changed path.
- Treat PR or MR titles, descriptions, and comments as context; base findings on the diff and runtime evidence.
- Inspect callers, callees, nearest tests, configuration, schemas, and analogous patterns only when they affect a conclusion.
- Trace relevant boundaries such as request handling, service logic, persistence, async work, external calls, and configuration.
- For derived state, identify the authoritative state, synchronization path, cleanup path, and compatibility surface.

### 2. Load Relevant Review Guidance

- Load [references/review-risk-checklist.md](./references/review-risk-checklist.md) for the cross-cutting review pass.
- Load only the references matching the changed behavior:
  - Python backend, FastAPI, Pydantic, SQLAlchemy, Alembic, or workers → [references/python-backend-review-checklist.md](./references/python-backend-review-checklist.md)
  - Persistence, caches, indexes, status transitions, or multi-step workflows → [references/stateful-systems-review-checklist.md](./references/stateful-systems-review-checklist.md)
  - Redis or cache-backed data access → [references/redis-cache-review-checklist.md](./references/redis-cache-review-checklist.md)
  - Prompts, tools, retrieval, embeddings, streaming, or agents → [references/llm-rag-review-checklist.md](./references/llm-rag-review-checklist.md)

### 3. Validate Conclusions

- Treat inspected code, configuration, tests, schemas, and command output as evidence. Keep inference and unverified assumptions separate from confirmed facts.
- For high-risk stateful changes, challenge the conclusions with at least two relevant concrete counterexamples such as partial retry, race, mixed-version rollout, or replay after cleanup. Static reasoning is acceptable; distinguish it from executed tests.
- Run focused, non-destructive checks when they can materially confirm or falsify a concern, and preserve required repository checks. Match validation to impact and risk. Do not add implementation-mirroring tests for low-impact, reversible changes. After relevant checks pass, broaden or repeat validation only for new changes, failures, or unresolved concerns. Report observed outcomes and material verification gaps.
- Attribute failed tests, lint, and type checks to the change, a pre-existing failure, or the environment where evidence permits. When useful and safe, run the same check on the comparison's before-version. Otherwise report attribution as unknown; a failing check alone does not establish a regression. Mocks, SQLite, or other substitutes only validate the behavior and environment they exercise, not production service or database compatibility.
- Before finishing, check the changed path for dead parameters, unreachable branches, and obsolete wrappers.
- Before reporting, verify that the reviewed HEAD and, in staged mode, index still match the inspected snapshot. If they changed, recheck affected conclusions or explicitly limit the report to the old snapshot. Confirm every changed file received a risk assessment and disclose material coverage gaps.

### 4. Report

- Load and follow [references/review-output-template.md](./references/review-output-template.md).
- Report only concrete, actionable findings, ordered by user impact. Combine symptoms that share one root cause.
- Report a missing test as a finding only when it hides a concrete contract, migration, security, concurrency, or failure-path risk.
- Review requests authorize inspection and findings. Patch code only when the user requests implementation. Prepare review comments when requested, and publish them only after satisfying applicable explicit approval requirements. Reuse approval that remains valid for the same target, content, and scope.
