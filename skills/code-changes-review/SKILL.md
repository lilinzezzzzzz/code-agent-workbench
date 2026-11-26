---
name: code-changes-review
description: Review Web frontend, Python backend, and cross-stack changes for correctness, compatibility, and maintainability. Invoke explicitly with $code-changes-review to review current unstaged changes (检查未暂存改动), current staged changes (检查暂存区), or the complete committed branch against a user-specified base before PR/MR submission. Individual commits, arbitrary diffs, localized checks, and debugging are outside this workflow.
---

# Code Changes Review

Turn a change set into evidence-backed findings. Prioritize correctness and operational risk over style.

## Review Principles

- Treat correctness, safety, and compatibility as constraints. Assess readability and maintainability in the context of business semantics, callers, existing interfaces, and project conventions.
- Simplify to reduce the cost of understanding and changing code: remove unnecessary concepts, state, branches, indirection, and dependencies. Fewer lines or denser expressions are not goals; function length, parameter count, nesting depth, and complexity scores are clues rather than findings.
- Recognize necessary business complexity. Favor local, incremental, easy-to-verify adjustments that preserve boundary cases, error handling, and business constraints. Recommend larger refactors only when concrete benefits and prerequisites justify their cost.
- Report material problems or improvements with a clear practical benefit. Follow existing conventions for stylistic choices; do not invent findings to fill a checklist.

## Scope Gate

- Select the mode from the user's request. `检查当前 unstaged 改动` selects unstaged review, and `检查当前 staged 代码` or `检查暂存区` selects staged review, even when a base was provided earlier. Use complete-branch mode for a pre-PR/MR review of the committed branch.
- If the mode is unclear, inspect workspace status read-only and ask the user to choose among the applicable modes. For unstaged review, mention non-ignored untracked files. For staged review, explain that it covers the index. Indicate whether each local scope has eligible changes. For complete-branch review, explain that it requires a base ref and invite the user to provide it with their choice. Recommend a mode with a short reason when the request and observed state support it. Wait for the user's choice before starting the review.
- Use normal code inspection for individual commits, arbitrary diffs, debugging, design-conformance, and localized reviews.
- Once the selected mode's prerequisites are satisfied, complete the authorized review and report without asking whether to proceed.
- Identify the reviewed snapshot before inspecting content. For branch mode, record the resolved base, merge-base, and HEAD commit SHAs. For staged mode, record HEAD (or its absence) and an index snapshot identifier, such as a tree ID obtained from a temporary copy of the index. For unstaged mode, capture the diff and untracked-file state described below. Preserve the real index and working tree during snapshot identification. If identification is unavailable, disclose the reproducibility limitation.

### Complete Branch

- Require a base branch or base ref explicitly provided or selected by the user, including an earlier instruction that remains applicable to this review. If missing, ask the user to choose. List relevant known candidates from the PR/MR target, repository conventions, or local refs. Label local and remote-tracking refs explicitly, such as `refs/heads/main` and `origin/main`. Recommend a candidate with a short reason when the available evidence supports it, and accept another base ref from the user. Wait for the user's selection before resolving the comparison range, fetching, or reviewing the branch delta.
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

### Unstaged Changes

- Review the index-to-working-tree delta from the repository root using `git --no-optional-locks diff --no-ext-diff --no-textconv --`. Include non-ignored untracked files as additions using `git ls-files --others --exclude-standard -z` and their working-tree content. Staged-only changes and ignored untracked files are outside this scope. This mode works without `HEAD` on an unborn branch and requires no base, fetch, `git add`, or stash.
- For a partially staged file, use the index version as the baseline and the working-tree version as the result. Tie findings to the unstaged hunks or untracked additions. Use surrounding code, including staged content, as context where it affects a finding.
- Detect unresolved index entries with `git ls-files --unmerged`. Report those paths as coverage gaps because they lack a single index baseline. Review the remaining in-scope changes without resolving conflicts. If there are no eligible changes, report that and stop.
- Identify the reviewed state using a digest of the tracked diff (add `--binary` when computing the digest) and a manifest of untracked paths with file types and content hashes. Attribute checks to the inputs they actually used, since tests run in the working tree can exercise staged changes too.

## Workflow

### 1. Understand the Change

- Read the diff summary, changed implementation, and relevant runtime path before judging intent.
- Inventory all changed files, including additions, deletions, renames, configuration, and generated artifacts. Assess each file's risk before selecting paths for deeper inspection. Read large or truncated diffs in batches; disclose uninspected portions rather than implying complete coverage. A per-file report is unnecessary.
- Establish intended behavior from applicable repository instructions, contracts, and accepted project decisions. Do not impose a preferred architecture or introduce universal redaction, retry, lock, or fallback requirements without a concrete risk in the changed path.
- For each material invariant affected by the change, connect the requirement to its enforcing runtime path and a concrete counterexample. Use this mapping to select deeper inspection and checks; no per-file matrix is required.
- For high-risk changes, identify the key assumption that must hold for affected consumers. Trace the most relevant counterexample through the actual consumer or boundary, including unchanged or indirect paths such as persisted data, serialized fields, or shared configuration. Record a material gap if the consumer or contract is unavailable.
- Treat PR or MR titles, descriptions, and comments as context. Tie each finding to evidence in the reviewed snapshot.
- Inspect callers, callees, nearest tests, configuration, schemas, and analogous patterns only when they affect a conclusion.
- When a change affects a browser-facing contract, trace the affected user action or view through the client and server, even if only one side changed. Use unchanged code in the reviewed snapshot as context. For example, check how a form serializes a cleared field and how the handler interprets that value. If a consumer is unavailable, identify the compatibility assumption.
- Trace relevant boundaries such as request handling, service logic, persistence, async work, external calls, and configuration.
- For derived state, identify the authoritative state, synchronization path, cleanup path, and compatibility surface.

### 2. Load Relevant Review Guidance

- Load [references/review-risk-checklist.md](./references/review-risk-checklist.md) for the cross-cutting review pass.
- Load the [shared code quality checklist](../_shared/code-quality-review-checklist.md) to assess complexity, readability, maintainability, and opportunities to simplify the changed implementation. Apply the relevant questions and the evidence and preservation checks in [Validate Conclusions](#3-validate-conclusions).
- Load only the references matching the changed behavior:
  - Browser UI, client state, rendering, or an API contract consumed by a Web frontend → [references/frontend-web-review-checklist.md](./references/frontend-web-review-checklist.md). Combine with the Python checklist when Python backend behavior is also affected. An unrelated frontend directory or a server-only JavaScript file does not trigger this checklist.
  - Python backend, FastAPI, Pydantic, SQLAlchemy, Alembic, or workers → [references/python-backend-review-checklist.md](./references/python-backend-review-checklist.md)
  - Persistence, caches, indexes, status transitions, or multi-step workflows → [references/stateful-systems-review-checklist.md](./references/stateful-systems-review-checklist.md)
  - Redis or cache-backed data access → [references/redis-cache-review-checklist.md](./references/redis-cache-review-checklist.md)
  - Prompts, tools, retrieval, embeddings, streaming, or agents → [references/llm-rag-review-checklist.md](./references/llm-rag-review-checklist.md)

### 3. Validate Conclusions

- Treat inspected code, configuration, tests, schemas, and command output as evidence. Keep inference and unverified assumptions separate from confirmed facts.
- Before reporting a material finding, test the weakest link in its reasoning. Check that the trigger is reachable under supported inputs or states and look for an existing guard, caller constraint, or contract that would prevent the claimed outcome. If the evidence cannot establish the core trigger or causal link, report it under Open Questions.
- Support maintainability conclusions with a concrete execution path, call relationship, or representative business-change scenario. Before recommending deletion, merging, or refactoring, check compatibility, boundary and error semantics, resource cleanup, and concurrency constraints. Explain the benefit, cost, and behavior that must be preserved.
- For high-risk stateful changes, challenge the conclusions with at least two relevant concrete counterexamples such as partial retry, race, mixed-version rollout, or replay after cleanup. Static reasoning is acceptable; distinguish it from executed tests.
- Run the smallest safe, non-destructive check that can confirm or falsify a material concern when the reviewed snapshot can be exercised. Use the real entry point or implementation and compare the observed result with the required behavior. Preserve required repository checks and match additional validation to impact and risk. Do not add implementation-mirroring tests for low-impact, reversible changes. After relevant checks pass, broaden or repeat validation only for new changes, failures, or unresolved concerns. Report observed outcomes and material verification gaps.
- Attribute failed tests, lint, and type checks to the change, a pre-existing failure, or the environment where evidence permits. When useful and safe, run the same check on the comparison's before-version. Otherwise report attribution as unknown; a failing check alone does not establish a regression. Mocks, SQLite, or other substitutes only validate the behavior and environment they exercise, not production service or database compatibility.
- Reconcile the material invariants with inspected evidence or explicit coverage gaps before concluding. Passing tests support only the scenarios exercised, not unchecked paths or operation sequences.
- Before finishing, check the changed path for dead parameters, unreachable branches, and obsolete wrappers. Inspect relevant callers and dynamic registration or configuration before calling code unused; report evidence gaps when its purpose cannot be established.
- Before reporting, verify the reviewed HEAD in branch and staged modes, the index snapshot in staged mode, and the captured diff and untracked-file state in unstaged mode. If the reviewed state changed, recheck affected conclusions or limit the report to the inspected state. Confirm every changed file received a risk assessment and disclose material coverage gaps.

### 4. Report

- Load and follow [references/review-output-template.md](./references/review-output-template.md).
- Start with a short overall judgment, then distinguish issues to address from optional improvements, ordered by actual impact within each category. Keep both concrete and actionable, and combine symptoms that share one root cause. End with the most valuable next action; apply the template's evidence prerequisites before recommending retaining the current implementation.
- Report a missing test as a finding only when it hides a concrete contract, migration, security, concurrency, or failure-path risk.
- Review requests authorize inspection, a report, and brief local examples where needed. Patch code only when the user requests implementation. Prepare review comments when requested, and publish them only after satisfying applicable explicit approval requirements. Reuse approval that remains valid for the same target, content, and scope.
