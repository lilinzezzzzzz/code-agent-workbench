---
name: git-code-reviewer
description: Review PRs, MRs, commits, diffs, or workspace changes for Python backend services. Use for code review, CR, PR/MR review, 风险审查, 代码审查, 找风险, or 审核实现; prioritize correctness, regressions, contract and data safety, concurrency, security, performance, and concrete test gaps.
---

# Code Review

Turn a change set into evidence-backed findings. Prioritize correctness and operational risk over style.

## Scope Gate

- Before resolving the comparison range, fetching a base, or reviewing code, require a base branch or base ref explicitly provided by the user. If missing, ask `基础分支是什么？` and do not begin the review. Do not infer it from PR metadata, repository defaults, the current branch, or local context.
- After receiving the base, load and follow [../_shared/git-remote-base-resolution.md](../_shared/git-remote-base-resolution.md) for ref resolution and freshness.
- Use the user-provided PR, MR, commit range, or diff as the review artifact. For workspace reviews, include tracked staged and unstaged changes by default.

## Workflow

### 1. Understand the Change

- Read the diff summary, changed implementation, and relevant runtime path before judging intent.
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
- For high-risk stateful changes, test at least two concrete counterexamples such as partial retry, race, mixed-version rollout, or replay after cleanup.
- Run focused, non-destructive validation when it can materially confirm or falsify a concern. Report what ran, what was skipped, and what remains unverified.
- Before finishing, check the changed path for dead parameters, unreachable branches, and obsolete wrappers.

### 4. Report

- Load and follow [references/review-output-template.md](./references/review-output-template.md).
- Report only concrete, actionable findings, ordered by user impact. Combine symptoms that share one root cause.
- Report a missing test as a finding only when it hides a concrete contract, migration, security, concurrency, or failure-path risk.
- Do not patch code or publish review comments unless the user explicitly asks.
