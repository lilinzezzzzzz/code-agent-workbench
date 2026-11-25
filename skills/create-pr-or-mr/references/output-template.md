# PR/MR Output Template

Use this template when the user requests a description and neither the user nor applicable repository instructions define its structure. Include only the requested title or description. Use as many points as the actual change needs; the sample rows are not a required count. Omit empty or redundant sections.

## Default

```markdown
基于 `<base-ref>` 生成。

基线说明：`<remote-tracking|local|explicit>`；fetch: `<executed|not-needed|degraded>`；base commit: `<resolved-sha>`

标题：
<title>

描述：
## 主要改动

- <概括核心改动 1>
- <概括核心改动 2>
- <概括核心改动 3>

## 技术说明

- <仅保留 reviewer 需要知道的技术细节、兼容性约束或实现取舍；无则可省略该节>
```

## Short

Use this version when the user asks for a shorter description.

```markdown
基于 `<base-ref>` 生成。

基线说明：`<remote-tracking|local|explicit>`；fetch: `<executed|not-needed|degraded>`；base commit: `<resolved-sha>`

标题：
<title>

描述：
- <改动点 1>
- <改动点 2>
- <改动点 3>
```

## Title Guidance

- Prefer one line.
- Use Chinese by default.
- Keep technical identifiers such as `AgentBuild`, `NodeConfig`, `origin/main`, `<remote>/<branch>`, or `tenant RPC` when they carry meaning.
- Prefer Conventional Commits-style PR titles by default, using `<type>(<scope>): <subject>` when scope adds real signal.
- Name the concrete change and any evidenced outcome. A precise technical title is appropriate when the change is technical; do not invent a business benefit or imply behavior changed when it did not.
- If the target repo clearly uses a different PR title convention, follow that convention instead of forcing Conventional Commits.

## Base Ref Guidance

- Always include the exact base ref near the top.
- Report the actual ref kind and resolved commit SHA. Fetch status describes freshness; it does not determine whether a commit SHA can be recorded. For an approved cached-ref downgrade, explicitly state that the ref may not match the latest remote branch.
- Use [../../_shared/git-remote-base-resolution.md](../../_shared/git-remote-base-resolution.md) for resolution, freshness, downgrade, and reporting rules.
