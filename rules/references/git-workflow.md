---
trigger: model_decision
description: Load for branches, staging, commits, cherry-picks, merges, rebases, resets, reverts, stashes, tags, remotes, fetches, pulls, pushes, or PR/MR history-sensitive work.
---
# Git Workflow Rules

Use these rules for repository history and remote state. Read-only status,
diff, log, and show commands are safe discovery; mutation must remain within
the user's requested workflow.

## Workspace Safety

- Inspect `git status --short`, the relevant staged/unstaged diff, current
  branch, and required refs before staging, committing, switching, fetching,
  pulling, cherry-picking, merging, rebasing, reverting, resetting, stashing,
  tagging, or pushing.
- Do not stage, stash, reformat, discard, or include unrelated work. If changes
  overlap, adapt around them or explain the concrete conflict.
- Do not use destructive reset, clean, checkout/restore, broad removal,
  history rewrite, or force push without explicit authorization and a stated
  recovery path. Prefer `git revert` for reversing published commits.
- Use non-interactive commands where practical; never bypass hooks or branch
  protection merely to make an operation succeed unless explicitly approved.

## Branches And Refs

- Follow repository naming and base-branch conventions. If none exists, use a
  concise semantic prefix such as `feature/`, `bugfix/`, `hotfix/`, `docs/`,
  `refactor/`, `test/`, `ci/`, `chore/`, or `release/`.
- Determine the repository's default branch from explicit user input,
  repository configuration or documentation, or the selected remote's symbolic
  HEAD. Support both `main` and `master`; never assume one exists. If multiple
  plausible default branches remain, report the candidates and ask which ref
  defines the workflow.
- Resolve ambiguous base names before computing diffs or changing history. For
  PR review, drafting, and restacking, an unqualified `main`, `master`, or
  `dev` normally means the up-to-date remote-tracking ref; report the resolved
  ref instead of silently relying on a stale local branch.

## Fetch, Pull, And Upstreams

- Verify the current branch, selected remote, upstream, default branch, and
  ahead/behind or divergence state before fetching or pulling. Do not pull from
  an inferred remote or while detached from a branch without an explicit plan.
- Fetch only when current remote state matters and network access is
  authorized. Do not imply a local remote-tracking ref is current without a
  fetch or other evidence.
- Prefer fetch followed by an explicit fast-forward, rebase, or merge so the
  history strategy is visible. Use `pull --ff-only` when the local branch should
  contain no unique commits; if branches diverged, follow repository policy or
  obtain the user's choice between rebase and merge.
- Inspect and preserve a dirty workspace before pull. Do not enable autostash,
  create a stash, discard changes, or choose a conflict strategy on the user's
  behalf merely to make pull succeed.

## Cherry-Pick

- Before cherry-pick, verify the destination branch, ordered commit list,
  source refs, workspace state, and whether any commit or equivalent patch is
  already present.
- Preserve the requested commit order. Do not cherry-pick a merge commit without
  an explicit mainline-parent decision, and do not silently skip an empty or
  duplicate commit without establishing why it is empty.
- On conflict, inspect the affected paths and operation state before resolving,
  continuing, skipping, or aborting. Preserve unrelated work and do not choose
  a semantic resolution from conflict markers alone.
- After completion, inspect the resulting commits and diff, verify required
  artifacts, and run checks appropriate to the transplanted behavior. Report
  original and new commit IDs when cherry-pick created new commits.

## Commits And Remote Actions

- Create a commit, cherry-pick, pull, push, tag, merge, or open/update a PR/MR
  only when the user explicitly requests that action or an explicitly invoked
  workflow includes it.
- Base commit messages on the staged diff or an explicit range. Before commit,
  verify the staged file list and inspect staged content for unrelated changes,
  secrets, generated noise, and incomplete required artifacts.
- Preserve repository commit-message and signing conventions. Do not amend a
  commit or rewrite shared history without explicit direction.
- Before push, report or verify the destination remote, branch, and upstream.
  Never force push by default; if approved, prefer `--force-with-lease` and
  confirm the expected remote ref.
