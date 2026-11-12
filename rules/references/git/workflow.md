# Git Workflow Rules

Use these rules for Git workspace safety, repository history, and remote state.
Read-only status, diff, log, and show commands are safe discovery; mutation
must remain within the user's requested workflow.

## Workspace Safety

- Create or switch branches, or create, switch to, or maintain worktrees,
  only when required by the user's requested workflow or explicitly requested
  by the user. If the agent proposes creating a new worktree and the user has
  not already authorized its creation, explain why it is needed and obtain
  user approval before creating it.
- When creating a new worktree, also create and check out a new task branch
  from the agreed starting ref, unless the user explicitly requests otherwise.
- Inspect `git status --short`, the relevant staged/unstaged diff, current
  branch, and required refs before staging, committing, switching,
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
- Name branches for the task's dominant intent. When naming from existing
  changes, inspect the real diff; when preparing work that has not started,
  use the requested task rather than inventing changes or requiring a diff.
- Use `docs/`, `test/`, `ci/`, or `refactor/` only when that concern describes
  the main purpose, not merely because related files are touched. In particular,
  `refactor/` implies preserved behavior; feature or fix work with supporting
  documentation or tests should retain the feature or fix prefix.
- Before creating a branch, validate its name and check for existing refs.
  Reuse only a branch that belongs to the intended task; otherwise choose a
  distinct name when the user has not fixed it. Do not reset or overwrite an
  existing branch merely to make creation succeed.
- Determine the repository's default branch only when the requested workflow
  depends on it. Use explicit user input, repository configuration or
  documentation, or the selected remote's symbolic HEAD; never assume `main`
  or `master`. If ambiguity would change the comparison or operation target,
  report the candidates and ask which ref to use. Missing default-branch
  information does not block work whose required refs are already explicit.
  Preserve workflow-specific requirements for a user-provided base.
- Resolve ambiguous base names before computing diffs or changing history. For
  PR review, drafting, and restacking, an unqualified `main`, `master`, or
  `dev` normally means the up-to-date remote-tracking ref; report the resolved
  ref instead of silently relying on a stale local branch.

## Fetch, Pull, And Upstreams

- Do not automatically inherit tracking of the base branch when creating a
  task branch. Set upstream from an established publication or tracking target,
  not merely a matching branch name. If that target is not established, leave
  upstream unset; configuring it does not authorize a push.
- Before fetch, verify the selected remote and required refs. Fetch only when
  fresh remote evidence matters and existing tool/network permissions and task
  scope allow it. Missing current-branch upstream or default-branch information
  does not block fetching an explicitly identified remote/ref. Preserve any
  explicit network approval requirement.
- Do not imply a local remote-tracking ref is current without a fetch or other
  evidence.
- Before integrating fetched changes, inspect the current branch, workspace,
  upstream, and divergence, and follow the authorized history strategy. Do not
  pull from an inferred remote or while detached from a branch without an
  explicit plan.
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

## Commit Messages

- Follow applicable user requirements and repository commit-message conventions.
  When no format convention is specified, default to
  [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
  This default is a workflow choice, not a requirement imposed by the specification.
- When using Conventional Commits, use
  `<type>[optional scope][optional !]: <description>`. Require a noun type label
  and a short, non-empty description after `: `. An optional scope is a noun
  naming a codebase area, enclosed in parentheses. Optional `!` goes immediately
  before `:`. Bracketed parts in this notation are not literal text.
- Use `feat` for new features and `fix` for bug fixes. Other types are allowed;
  common type lists are not closed enums required by the specification.
- Mark breaking changes of any type with `!`, an uppercase
  `BREAKING CHANGE: <description>` footer (equivalently `BREAKING-CHANGE:`),
  or both. Whenever `!` is used, describe the breaking change in the title as
  well; a footer is optional. Migration guidance may go in the body or footer.
- Body and footers are optional. Separate a body or footer section from the
  title with a blank line, and a footer section from a preceding body with a
  blank line. Bodies are free-form; footers use a
  word token followed by `: ` or ` #` and a string value. Replace whitespace
  in tokens with hyphens, except for `BREAKING CHANGE`. Footer values may span
  lines until the next valid footer token/separator pair.
- Language, lowercase types, imperative wording, final punctuation, and length
  limits are writing or repository conventions, not specification requirements.
  Apart from the uppercase breaking-change footer tokens, do not reject tokens
  solely for casing. Preserve code identifiers as written.

## Commits And Remote Actions

- Create a commit, cherry-pick, pull, push, tag, merge, or open/update a PR/MR
  only when the user explicitly requests that action or an explicitly invoked
  workflow includes it.
- Base message drafts on the user-designated diff or explicit range, defaulting
  to the staged diff. Drafting does not authorize staging or committing those
  changes. Before commit, verify the final staged file list and inspect staged
  content for unrelated changes, secrets, generated noise, and incomplete
  required artifacts; ensure the message describes the final staged scope.
- When the requested workflow includes staging and it is already authorized
  for a clear scope, stage only those changes and re-inspect the final staged
  diff. Do not pause merely because nothing was initially staged; without
  staging authorization, do not choose files to stage automatically.
- Preserve repository signing conventions. Do not amend a commit or rewrite
  shared history without explicit direction.
- Before push, report or verify the destination remote, branch, and upstream.
  Never force push by default; if approved, prefer `--force-with-lease` and
  confirm the expected remote ref.
