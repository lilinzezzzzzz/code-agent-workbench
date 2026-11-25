# Commit Message Template

These examples use Conventional Commits. Follow the skill's format policy and adapt the output to other applicable user or repository conventions. Keep it compact unless the change genuinely needs more structure.

The label `建议的 commit message:` is response text, not part of the commit message. Keep it outside the copyable message block; pass only the message to Git. Placeholders below are illustrative, not literal text to commit.

## Draft Only

Use when the user asked for a message but not for an actual commit.

建议的 commit message:

```text
<type>(<scope>): <subject>
```

If `scope` is unnecessary, omit it:

建议的 commit message:

```text
<type>: <subject>
```

## Draft With Body

For body-writing guidance, see [commit-type-selection.md](./commit-type-selection.md#body-rules). This example uses bullets; prose and multiple paragraphs are also valid.

建议的 commit message:

```text
<type>(<scope>): <subject>

- <body bullet 1>
- <body bullet 2>
```

## Draft With Breaking Change

The examples below illustrate the breaking-change forms defined in the skill's contract.

建议的 commit message:

```text
feat(api)!: 将订单查询响应改为分页结构

BREAKING CHANGE: GET /orders 从数组改为包含 items 和 total 的对象；调用方需从 items 读取订单列表
```

An explicit subject can stand alone; `!` does not require a body or footer:

```text
build!: 将最低 Node.js 版本提升至 22
```

The footer alone also marks a breaking change, without `!` in the title:

```text
feat(config): 支持通过 API_URL 配置完整服务地址

BREAKING CHANGE: 移除 API_HOST 和 API_PORT；请改用 API_URL
```

## Draft With Footers

Use a blank line before the footer section. The issue number below is illustrative; include real references only when supported by evidence.

```text
fix(api): 修复并发更新覆盖订单状态的问题

使用版本条件更新订单，冲突时返回可重试错误。

Refs: #123
```

When multiple footers are warranted, place each on its own line without requiring a blank line between them:

```text
feat(config)!: 用 API_URL 替代拆分的服务地址配置

BREAKING-CHANGE: 移除 API_HOST 和 API_PORT
请将这两个配置项合并为包含协议、主机和端口的 API_URL。
Refs: #123
```

This last example uses the equivalent `BREAKING-CHANGE` token and a multiline value, which ends when the next footer (`Refs`) begins.

## Commit Executed

Use only after observing successful commit creation and verifying the resulting commit. A request to commit or an attempted command is not evidence of success.

```text
已提交：<commit-sha>

<exact commit message>

<仅在相关时说明剩余改动>
```

If useful, explain an evidence-backed classification choice briefly. Do not report commit-scope uncertainty as an assumption after committing. Resolve material scope ambiguity before execution.

## Blocked Cases

### Nothing staged

Follow the [workflow's evidence and staging rules](../SKILL.md#workflow). If execution cannot proceed, explain the specific missing evidence or authorization and keep any prepared message labeled as a draft. An initially empty index alone is not a blocker when staging is already authorized for a clear scope.

### Mixed concerns

```text
当前 staged changes 包含多个无关关注点，不建议强行生成单一 commit message。
建议先拆分或重新 stage，再提交。
```

## Example Messages

```text
feat(auth): 添加 JWT 刷新令牌接口
fix(api): 修复分页参数为空时的 500 错误
refactor(vector): 拆分 embedding client 初始化逻辑
perf(db): 减少知识库列表接口的 N+1 查询
test(chunk): 补充分块任务失败重试场景覆盖
chore: 更新开发环境 pre-commit 配置
```
