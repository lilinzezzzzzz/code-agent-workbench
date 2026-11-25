---
name: rename-worktree-chat
description: 为 Codex 主聊天标题加上其 worktree 标识。用于用户要求重命名主聊天并保留 worktree 路径标识的场景，包括从侧边聊天发起的请求。
---

# 用 worktree 标识重命名主聊天

1. 确认目标聊天。从侧边聊天收到“主聊天”或“main chat”的请求时，使用父聊天引用中的 `threadId` 和 `hostId`。在主聊天直接收到请求时，使用当前聊天的标识。用 `read_thread`（`includeTurns: false`）读取目标标题与 `cwd`。需要通过 `list_threads` 查找时，只在现有上下文能唯一确定目标的情况下继续。
2. 从目标聊天的 `cwd` 提取标识。
   - 路径中有名为 `worktrees` 的目录时，取它下一级的目录名。例如 `~/.codex/worktrees/1f51/docflow` 和 `~/.codex/worktrees/1f51/docflow/src` 都取 `1f51`。
   - 路径中没有 `worktrees` 目录时，取倒数第二级目录名。例如 `~/Developer/local-workspace/code-agent-workbench` 取 `local-workspace`。
   - 如果缺少 `cwd` 或对应层级没有目录名，向用户确认路径或标识。
3. 默认用 `[<worktree 标识>] <原标题>`。用户提供新标题时，用新标题代替原标题。标题已有同一前缀时保留单个前缀。最终标题与当前标题一致时，直接报告现有标题。
4. 用户要求执行重命名时，用 `set_thread_title` 并显式传入目标聊天的 `threadId`。核对工具返回的聊天 ID 和标题，并向用户报告最终名称。用户只要求拟标题时，直接返回建议标题。
