---
trigger: model_decision
description: Load for worktree selection, creation, reuse, transferring active work between worktrees, shared-worktree coordination, environment isolation, removal, or metadata cleanup.
---
# Git Worktree Rules

Use these rules for task workspace lifecycle and worktree-specific safeguards.
Follow the global authorization and user-work protection boundaries. This
reference applies without requiring a worktree skill to be installed.

Load `git/workflow.md` through the active assistant's reference path when the
operation also involves branch creation, switching or deletion, base/ref resolution,
staging, stashing, history changes, or remote actions. Simple workspace
inventory or reuse does not require it unless one of those operations is needed.

## Worktree-First Task Workspaces

- Prefer one stable primary worktree plus short-lived task worktrees, with one
  task branch per worktree. Keep the primary on the repository's established
  default or integration branch; do not assume `main` or switch an existing
  workspace merely to enforce this convention.
- When selecting a task workspace, inspect workspace status and
  `git worktree list` to decide whether to reuse a task workspace or create one.
  Reuse an existing worktree for the same task under the coordination rules
  below. Resolve a creation base only when a new task branch is needed. Choose
  routine branch names and paths from task context and repository conventions.
  If a missing base decision materially changes the starting content and
  cannot be resolved from evidence, ask a focused question while continuing
  independent preparation. Creating a local task branch and worktree is normal
  preparation for an authorized change request, subject to applicable explicit
  approval requirements.
- Respect explicit user or repository workflows, including an explicitly
  invoked skill's branch workflow. Continue ongoing work in its assigned
  directory. Read-only inspection does not require a new worktree; use a
  separate, optionally detached worktree when read-only review or temporary
  validation needs another revision checked out. Do not automatically stash,
  copy, or move uncommitted work to populate a new worktree; it starts from a
  commit, not another workspace's diff.
- Before transferring active work to another worktree, check the source for
  staged and unstaged changes and untracked files, regardless of whether the
  destination serves the same task. If any exist, show a concise change summary
  and destination path, then ask whether to leave them in place (recommended),
  stash selected changes only, or stash and restore them at the destination.
  Resolve which untracked files to include; handle ignored files separately.
  Do not stash, migrate changes, or start work at the destination until this
  decision is resolved. Reuse an explicit decision that remains valid for the
  same scope and destination. Continue independent checks and preparation while
  waiting, and identify this requirement when asking. Merely creating a
  worktree, inspecting another directory, or running read-only checks does not
  trigger this confirmation. An instruction to create or enter a worktree alone
  does not decide how to handle uncommitted changes.
- Place task directories outside the repository working directory, as siblings
  such as `../repo-feature-login` or under an external `../worktrees/repo/`
  parent. Follow existing naming conventions, keep branch-to-path mapping
  recognizable, and check for path collisions before creation.
- When creating a task worktree, create a new task branch with it by default.
  Resolve the base and any fetch under the applicable `git/workflow.md`
  rules. Explicitly specify the
  branch, path, and base: `git worktree add -b <branch> <path> <base-ref>`.
  If the task branch already exists, use `git worktree add <path> <branch>`
  instead of creating another branch. If it already has a worktree, prefer
  reusing that worktree under the coordination rules below; do not force a
  duplicate checkout. Detached worktrees for read-only review or temporary
  validation do not require a new branch.
- Isolate worktrees by task or branch, not by agent. When delegation is
  supported and permitted, multiple agents may share a worktree with clear
  file or module ownership. Serialize overlapping edits and Git mutations,
  and coordinate checks that depend on shared workspace state. Use separate
  worktrees for independent tasks or when concurrent changes cannot be safely
  coordinated. This rule does not itself authorize delegation or require
  splitting a task.
- Run edits, builds, and checks in the assigned directory and report its path
  and branch at handoff. Worktrees share Git refs and repository metadata;
  coordinate ref-changing operations across worktrees as well. Do not remove
  a worktree while another agent is using it; follow the cleanup rules below.
- Keep mutable environments and build outputs local to each worktree, including
  `.venv`, `node_modules`, `target`, `build`, and `dist`, unless the project
  explicitly supports safe sharing. Prefer the project's bootstrap process or
  example configuration. Ignored and untracked files such as `.env` are not
  copied by Git; do not blindly copy credentials or symlink another worktree's
  environment. Follow existing credential and access-control boundaries.
- Treat task worktrees as short-lived, but preserve them until work is handed
  off and cleanup is authorized. Before removal, check status including
  untracked and ignored files, unique commits, and active processes or agents.
  Use `git worktree remove <path>`, not direct filesystem deletion or forced
  removal. Delete a branch with `git branch -d <branch>` only when deletion is
  authorized and its work is confirmed integrated into the intended target;
  retain unmerged branches. Inspect stale entries with
  `git worktree prune --dry-run` before authorized metadata cleanup, and verify
  the resulting inventory with `git worktree list`.
