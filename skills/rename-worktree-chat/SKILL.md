---
name: rename-worktree-chat
description: 为 Codex 主聊天标题加上工作区标识。用于用户要求按主工作区或 worktree 标识重命名主聊天的场景，包括从侧边聊天发起的请求。
---

# 用工作区标识重命名主聊天

1. 确认目标聊天。从侧边聊天收到“主聊天”或“main chat”的请求时，使用父聊天引用中的 `threadId` 和 `hostId`。在主聊天直接收到请求时，使用当前聊天的标识。用 `read_thread`（`includeTurns: false`）读取目标标题与 `cwd`。需要通过 `list_threads` 查找时，只在现有上下文能唯一确定目标的情况下继续。
2. 按[共享标题规则](../_shared/worktree-chat-title.md)，根据目标聊天的 `cwd` 计算标签和标题。无法确定标签时，向用户确认路径或标签。
3. 用户要求执行重命名时，按共享规则更新并核对标题，报告最终名称。用户只要求拟标题时，返回建议标题。
