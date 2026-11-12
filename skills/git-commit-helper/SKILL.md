---
name: git-commit-helper
description: 基于 staged changes、指定 diff 或明确的提交范围，遵循适用的用户和仓库提交约定，默认采用 Conventional Commits 生成 commit message，并在用户明确要求提交代码时执行安全的提交流程。当用户要求写 commit message、总结 staged changes、帮忙提交代码、判断 type 或 scope、拆分提交边界时使用此 skill。
---

# Git Commit Helper

Use this skill to derive a commit message from the actual change set. Prefer one atomic commit, one clear subject, and no hidden assumptions.

## Core Rules

These are the skill's evidence and execution rules, not additional Conventional Commits syntax requirements.

1. Inspect the real change set before proposing or creating a commit.
2. Use the change set explicitly designated by the user. When no scope is designated, use staged content by default. Keep provided diffs, committed ranges, staged changes, and unstaged changes distinct; do not silently substitute or combine them. A message drafted from another range does not authorize staging or committing that range.
3. Do not auto-push or rewrite history unless the user explicitly asks for the corresponding action.

## Conventional Commits Contract

Follow applicable user requirements and repository commit-message conventions. When no format convention is specified, default to [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/). The contract below applies when using Conventional Commits; adapt the classification guidance and templates to other applicable formats.

```text
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

Square-bracketed parts above are optional notation, not literal text. This skill calls the short `description` the subject.

- Require a type (a noun label such as `feat` or `fix`) and a non-empty short subject immediately after the prefix's ASCII colon and space (`: `). An optional scope is a noun naming a codebase area, enclosed in parentheses. Put optional `!` immediately before the colon: `feat(api)!: ...` or `feat!: ...`.
- Use `feat` for a new feature and `fix` for a bug fix. Other types are allowed; the common types in the selection guide are not a closed list mandated by the specification.
- Body and footers are optional. Separate the subject from any body or footer with a blank line, and separate a footer section from a preceding body with a blank line. A body may contain free-form paragraphs or bullets.
- Mark breaking changes with `!`, a `BREAKING CHANGE: <description>` footer, or both. Any type can carry a breaking change. Whenever `!` is used, the subject must describe the breaking change, whether or not a footer is also present. Additional compatibility or migration context may go in the body or a footer. `BREAKING-CHANGE:` is an equivalent footer token.
- Follow the footer syntax in [references/commit-type-selection.md](./references/commit-type-selection.md). Keep `BREAKING CHANGE` and its equivalent `BREAKING-CHANGE` token uppercase. Apart from these breaking-change tokens, do not reject type, scope, or footer tokens solely for casing; for example, `FIX(parser): ...` is valid. Lowercase types and consistent scope casing are this skill's defaults. Preserve the exact casing of code identifiers and prose where it carries meaning.
- The language policy below and the writing suggestions in the selection guide are defaults, not additional specification requirements.

## Language Policy

Commit message 的 subject 和 body 默认使用中文，`type` 和 `scope` 默认使用英文；用户明确要求或适用的仓库提交规范另有规定时，遵循该要求。技术术语与代码标识符保留更准确的形式。

**示例：**

- `feat(auth): 添加 JWT 刷新令牌接口` ✓
- `fix(api): 修复分页参数为空时的 500 错误` ✓
- `feat(auth): add JWT refresh token endpoint` — 用户明确要求英文或仓库采用英文提交规范时适用。

## Workflow

1. Determine the user's intent.
   - `写 commit message` or `生成提交信息`: inspect the change set and draft the message only.
   - `看 staged changes`: summarize the staged diff and propose one strong message.
   - `提交代码`: inspect staged changes, generate the message, and commit if the staged scope is coherent.

2. Gather evidence from git.
   - Inspect the designated change set. For staged content, prefer `git status --short`, `git diff --staged --stat`, and `git diff --staged`.
   - If nothing is staged, check whether the user supplied a diff or explicit range. Use that evidence for a message-only request.
   - If committing is requested and staging is already authorized for a clear scope, inspect the relevant unstaged or untracked content, stage only the authorized changes, and re-inspect the final staged diff. Do not pause merely because nothing was initially staged.
   - If nothing is staged and staging is not authorized, explain the prerequisite without choosing files to stage. Complete any message preparation supported by the designated scope.
   - If the user provides a base branch or base ref for context, load [../_shared/git-remote-base-resolution.md](../_shared/git-remote-base-resolution.md) and follow its resolution, freshness, and reporting rules before using it.

3. Classify the change.
   - Load [references/commit-type-selection.md](./references/commit-type-selection.md).
   - For Conventional Commits, determine `type`, optional `scope`, optional breaking-change marker `!`, `subject`, optional `body`, and optional footers. Otherwise use the applicable format.

4. Check commit quality.
   - Check that the selected change set supports a coherent message; before committing, ensure the final staged diff represents one authorized concern and the message describes it. Do not include unrelated staged changes.
   - Check whether the change is breaking, revert-like, dependency-only, test-only, docs-only, or mixed.
   - Check the message against the applicable format policy, using the contract above when Conventional Commits applies.
   - Resolve low-risk type, scope-label, and wording choices from the evidence and state a material assumption briefly when useful. If ambiguity affects which changes are authorized, commit boundaries, or breaking-change meaning, ask a focused question before committing. Continue independent inspection and prepare concrete message or split recommendations.

5. Verify execution when a commit was requested.
   - Observe the command result and inspect the resulting commit, including its SHA, message, and committed scope, before reporting success.
   - Inspect remaining staged and unstaged changes without altering them.
   - If execution fails or its result is ambiguous, inspect the current state before retrying. Do not repeat a possibly completed commit, bypass hooks, or amend history merely to obtain success. Report the specific blocker and continue independent authorized work.

6. Produce the result in a stable shape.
   - Use [references/commit-message-template.md](./references/commit-message-template.md) as the default output shape.
   - When committing, show the exact message used.
   - When a base ref was used for context, state the exact base ref, whether it was remote-tracking or local, whether fetch was executed, and the fetched base commit SHA when fetch succeeded.
   - If you did not commit, label any message as a draft or recommendation and state any execution blocker accurately.
