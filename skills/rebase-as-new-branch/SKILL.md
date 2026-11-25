---
name: rebase-as-new-branch
description: Recreate the current git branch on top of an explicitly provided base branch by rebasing the branch-only commits onto a new versioned branch. The original source branch stays untouched. Use when retargeting a feature branch onto updated base history, including workflows like `A` 到 `A-v2` or `A-v2` 到 `A-v3`. Treat unqualified base names as remote-tracking branches by default. Require a user-provided base before base-dependent planning or execution. Show the specified base and obtain approval for the concrete restack plan before applying.
---

# Rebase as New Branch

Rebuild the current branch on top of an explicitly specified base branch while preserving the branch's own commits. A new versioned branch (`A` → `A-v2`, `A-v2` → `A-v3`) is created so the original source branch stays intact and recoverable.

For base ref resolution, freshness, and downgrade reporting, load and follow [../_shared/git-remote-base-resolution.md](../_shared/git-remote-base-resolution.md).

## Workflow

1. **Require base branch** — Use a base explicitly provided by the user, including an earlier instruction that clearly remains applicable. If missing, ask `基础分支是什么？` and briefly identify this requirement. Do not infer the base, resolve the comparison range, fetch, or begin restack execution. Independent read-only preparation may continue.
2. **Show base** — Once provided, visibly show the specified base (e.g. `基础分支：dev`) before base-dependent planning or execution.
3. **Plan** — Resolve `<skill-dir>/scripts/restack_from_base.py` and run it in plan mode. Fetch the base first (use `--skip-fetch` only if user explicitly allows). Resolve unqualified base to `<remote>/<base>` (prefer `origin`; ask if multiple non-`origin` remotes). Never silently fall back to a local branch.
4. **Report & confirm** — Load and follow [references/base-ref-resolution.md](./references/base-ref-resolution.md) for the concrete approval plan. Resolve material warning-related choices first, then present the resulting plan and every plan `warning:` line together. Obtain one explicit confirmation for that plan; do not repeat approval for warnings already covered.
5. **Apply** — Run `--apply --confirm` only after confirmation and after establishing that the execution path preserves the approved plan. The script creates the new branch with `git switch --no-track -c <new_branch> <source_branch>` and rebases with `git rebase --empty=drop --onto <base_ref> <base_ref>`. Never cherry-pick.
6. **Verify** — Apply the Verification criteria below before reporting success.
7. **Optional source cleanup** — Restack is complete after successful verification. Retain the source branch by default. If the user requests cleanup, follow Source Branch Deletion below. Pending or declined cleanup does not make the restack incomplete.

## Pre-conditions

- Abort if working tree is dirty (unless user explicitly asks to proceed).
- Abort if no branch-only commits to rebase (`<base_ref>..<source_branch>` is empty).
- Use `git log --reverse <base_ref>..<source_branch>` semantics for commit discovery.
- Approval applies to the concrete plan defined in [references/base-ref-resolution.md](./references/base-ref-resolution.md). Before mutation, establish that execution will use that plan. Matching ref names or freshness labels alone is insufficient. If a material input changes, show the changed plan and obtain renewed confirmation; otherwise reuse the existing approval. Do not apply through an execution path that cannot preserve this boundary.

## Naming Rule

- No `-v<integer>` suffix → append `-v2` (e.g. `feature/foo` → `feature/foo-v2`).
- Has `-v<integer>` suffix → increment (e.g. `feature/foo-v2` → `feature/foo-v3`).
- Do not guess a different scheme unless the repo uses one and the user asks.

## Commands

```bash
python3 <skill-dir>/scripts/restack_from_base.py --base dev          # plan mode (default)
python3 <skill-dir>/scripts/restack_from_base.py --base dev --apply --confirm  # apply after confirmation
```

Key flags: `--remote <name>`, `--source-branch <name>`, `--new-branch <name>`, `--base-ref <ref>`, `--skip-fetch`, `--confirm` (required with `--apply`).

The current script rebuilds the plan during apply; `--confirm` alone does not bind execution to the previously reviewed SHAs. The commands above describe the operation, not proof that the approval boundary is enforced. If that boundary cannot be established, report the limitation and pause mutation.

If the script is missing, check `<skill-dir>/scripts/` and retry with the resolved path. Manual fallback (last resort): `git switch --no-track -c <new_branch> <source_branch>` then `git rebase --empty=drop --onto <base_ref> <base_ref>`. A fallback must preserve the same approved-plan boundary and other preconditions.

## Rebase Warnings

Surface every plan warning and resolve material choices before the single apply confirmation. If a later choice changes the plan, show the change and renew only the affected approval:

- **Merge commits** → flattened by default. Ask: proceed, or abort and rerun with `--rebase-merges --empty=drop --onto <base_ref> <base_ref>`.
- **GPG-signed commits** → signatures dropped. Ask: proceed, rerun with `-S`, or abort. Never silently re-sign.
- **Other local branches in range** → left on pre-rebase commits. List affected refs. Ask: proceed, rerun with `--update-refs` (git 2.38+), or abort. Never pass `--update-refs` automatically.
- **Rebase conflict** → pause history-changing actions. Inspect the current operation state, conflicted files, relevant contracts, and available tests. Report the cause, unresolved semantic choices, and a concrete proposed resolution with supporting evidence. Cite this pause requirement. Do not edit conflicted files, continue, skip, or abort until the user explicitly authorizes the chosen recovery action. Reuse recovery approval that remains valid, and continue independent read-only diagnosis.
- `--empty=drop` is always used. New branch first push needs no `--force`. SHAs are rewritten.

## Source Branch Deletion

Retain the source branch unless the user requests cleanup. After successful restack and verification, prepare the exact refs and obtain separate explicit deletion approval. Approval must distinguish local deletion from remote deletion. Show exact refs:

- Local: `refs/heads/<source_branch>`
- Remote: upstream from `git for-each-ref --format=%(upstream:short) refs/heads/<source_branch>`, or `<remote>/<source_branch>` when unambiguous

Delete only after explicit confirmation:

```bash
git branch -D <source_branch>
git push <remote> --delete <remote_branch>
```

Rules: never delete if restack failed/conflict/unverified; HEAD must be on new branch; no remote ref → delete only local after confirming; multiple candidates → ask which.

## Verification

```bash
git status --short
git log --oneline --decorate --graph -n 15
git log --reverse <new_branch> --not <base_ref> --oneline
```

The commands above are inspection aids, not sufficient evidence by themselves. Verify against the approved plan:

- HEAD is on the new branch, the approved base commit is an ancestor of it, and the source ref still points to its recorded pre-operation SHA.
- Account for the selected changes, including rewritten commits, intentionally flattened merges, and omitted commits whose changes are already represented or became empty. Explain omissions with evidence; do not require unchanged SHAs or identical commit counts. Treat unexplained content loss as failed verification.
- Run relevant checks for integration or conflict-resolution risk and report what remains unverified. Follow applicable verification stopping conditions rather than repeating checks without new changes, failures, or unresolved concerns.

## Reporting

Report the approved plan and base freshness fields, observed execution and verification outcomes, rewritten commits and explained omissions, and material unresolved risks. State restack status separately from optional cleanup status; retained source branches do not imply incomplete restack. Avoid repeating plan details that have not changed unless needed to understand the result.

## References

- [../_shared/git-remote-base-resolution.md](../_shared/git-remote-base-resolution.md) — shared base-ref resolution, freshness, and reporting rules.
- [references/base-ref-resolution.md](./references/base-ref-resolution.md) — restack-specific confirmation and reporting rules.
