---
name: git-create-worktree
description: 为任务创建或复用 Git worktree，默认同时创建任务分支，并明确 branch、path 和 base。用于“创建 worktree”“为任务准备独立工作目录”或已授权任务需要工作区隔离的场景，不限于功能开发。仅在当前目录切分支、提交、restack 或清理 worktree 时不使用。
---

# Git Create Worktree

Create or reuse a task workspace while preserving source work. Apply the
keep-or-stash confirmation only under Leaving The Current Worktree below.
This skill prepares the workspace; it does not authorize commits, pushes,
history integration, cleanup, or delegation. Respect applicable repository
instructions and explicit workflow approval requirements.

## Select The Workspace

1. Inspect the repository root, current branch, `git status --short`, relevant
   staged and unstaged diffs, and `git worktree list --porcelain`. Establish
   which branch and workspace belong to the requested task. A dirty source
   workspace does not by itself prevent creating a worktree from a commit.
   Explain that staged and unstaged changes, untracked files, and ignored
   files remain in the source workspace and do not enter the new worktree.
   Do not automatically commit, stash, copy, or move them. Before transferring
   active work to another worktree, follow Leaving The Current Worktree below.
2. Prefer reusing the task's existing worktree unless the user explicitly
   requests relocation; follow the relocation flow in Create Or Reuse below.
   If only its branch exists,
   create a worktree on that branch. Otherwise create a new task branch and
   worktree together. Read-only review or temporary validation may use a
   detached worktree; ordinary inspection needs no new directory.
3. For a new branch, use the user's explicitly specified base; otherwise
   default to the current source worktree's `HEAD` commit, including when it
   is detached. Do not ask for a base merely because none was specified or
   silently substitute a default or integration branch. Verify the selected
   ref and record its commit ID; report the source branch or detached state.
   If `HEAD` has no commit yet, explain the missing prerequisite rather than
   inventing a base or creating an initial commit. Using local `HEAD` requires
   no fetch. For an explicit base, fetch only when fresh remote evidence
   matters and the task and permissions allow it; do not call an unfetched
   remote-tracking ref current. An existing task branch needs no separate
   creation base. For detached review, verify the requested revision instead.
4. Infer routine branch names from the requested task and repository naming
   conventions; an existing diff is not required. Prefer an external sibling
   directory such as `../repo-fix-payment` or an established external worktree
   parent. Check the absolute path, permissions, branch-name validity, and
   collisions. An unrelated same-name branch is not a reusable task branch;
   choose a distinct name when the user has not fixed it.

If missing information materially changes the starting content or target and
cannot be resolved from evidence, ask one focused question and continue
independent inspection. Do not request approval merely for a routine name or
path choice. For an authorized creation request or in-scope task preparation,
briefly state the chosen path, branch, and base/revision and proceed unless an
applicable instruction explicitly requires approval. In that case, prepare
the concrete command first, cite the requirement, and reuse valid approval.
For explanation or planning requests, report the result without creating it.

## Create Or Reuse

The following are command templates; substitute verified values and quote
paths and refs as shell arguments. Run from the source repository.
Use the verified commit ID for `<base-ref>` so concurrent source-branch
changes cannot silently change the chosen starting commit.

```bash
# New task branch; avoid accidentally tracking the base branch.
git worktree add --no-track -b <branch> <path> <base-ref>

# Existing local task branch, not checked out elsewhere.
git worktree add <path> <branch>

# Read-only review or temporary validation at a specific revision.
git worktree add --detach <path> <revision>
```

If the task branch exists only remotely, verify the remote-tracking ref and
create its local task branch with explicit tracking only when that remote
branch is the intended upstream. Do not infer this from the new branch's base.
If the branch is already checked out, prefer reusing its worktree unless the
user explicitly requests relocation. To relocate while retaining that branch,
prepare the destination path, change-handling plan, and the source worktree's
resulting branch or detached state together. Include any required source
branch transition in the same approval request; approval to stash or restore
changes alone does not authorize that transition. Reuse existing authorization
that covers the concrete plan. After the required decision is resolved and
selected changes are safely saved, release the branch through the authorized
source transition, then create the destination worktree on that branch and
restore changes only as agreed. Preserve any changes left in the source; if
the transition would endanger them, resolve that dependency rather than
forcing it. Do not silently create a replacement task branch.

Never force a duplicate checkout, reset an existing branch with `-B`, or
overwrite an occupied directory to make creation succeed. After an ambiguous
failure, inspect worktree, branch, and filesystem state before retrying; do not
automatically delete partially created resources.

Multiple agents may share a task worktree when delegation is permitted and
edits are coordinated. Establish file or module ownership, serialize
overlapping edits and Git mutations, and coordinate checks of shared state.
Use separate worktrees for independent tasks or uncoordinated concurrent work.
Git refs and repository metadata remain shared across worktrees.

## Leaving The Current Worktree

- Before starting work in another worktree, check the source for staged and
  unstaged changes and untracked files, whether or not it is the same task.
  If any exist, show their summary and the destination path. Ask once whether
  to leave them in place (recommended), stash selected changes only, or stash
  and restore them at the destination. Specify the selected scope, including
  untracked files; ignored files require separate handling. Cite this section
  as the confirmation requirement. Reuse an explicit decision that remains
  valid for that scope and destination; creating or entering a worktree alone
  does not imply a keep-or-stash decision.
- Until that decision is resolved, do not stash, migrate changes, or begin
  work at the destination. Continue independent inspection and preparation.
  Merely creating a worktree, inspecting another directory, or running
  read-only checks does not trigger confirmation. If the user keeps changes
  in place, preserve them and do not treat them as present at the destination.
- When stash is authorized, save only the agreed changes with a descriptive
  message and record the created stash's exact object ID before applying it.
  Coordinate access to shared stash state with other agents. Only restore at
  the destination when that was selected. Before applying, inspect its current
  state and read the instructions applicable to the destination and affected
  paths. Resolve any material conflict with the approved transfer before
  mutation, while continuing independent preparation. Then use
  `git stash apply --index <stash-id>` and verify content, staged state,
  and selected untracked files. Retain the stash for recovery until verification
  and authorized cleanup; do not use `pop` or automatically discard it. If
  saving or applying fails, inspect the resulting state before retrying, and
  resolve material conflicts without overwriting unrelated work.

## Verify And Continue

- Verify the inventory, target branch (or detached state), initial commit,
  and target status with `git worktree list --porcelain` and `git -C <path>`
  commands. For a new workspace, confirm its initial commit matches the
  selected source commit. For reuse, inspect its actual state without
  resetting it to a base. Verify that source changes either remain in place
  or are saved and, if requested, restored according to the user's decision.
  Preserve the source branch unless changing it was authorized. Do not mistake
  another agent's concurrent edits for your own results.
- Use the target directory explicitly for subsequent commands and read its
  applicable repository instructions before continuing. Report the absolute
  path, branch or detached revision, whether it was created or reused, and
  any preparation still needed. If workspace creation supports a larger
  authorized task, continue that task rather than stopping at this handoff.
- Keep mutable environments and build outputs isolated per worktree. Follow
  project bootstrap guidance when needed for the requested task; do not
  blindly copy secrets or symlink another worktree's environment. Workspace
  creation alone needs Git state checks, not an application test suite or
  dependency installation. Leave the worktree available for the task;
  cleanup is a separate authorized operation.
