# Rules

本目录维护跨项目的 agent 行为基线和按需加载的技术规则。任务专属流程见
[Skills](../skills/README.md)，assistant 运行配置见
[Configs](../configs/README.md)。

`baseline.md` 是仓库中的源文件名；同步后使用各 assistant 识别的 `AGENTS.md`
作为目标文件名。两者内容一致，维护时修改源文件后再同步。

## 内容与加载方式

| 路径 | 用途 |
| --- | --- |
| [baseline.md](baseline.md) | always-on 入口：指令优先级、授权边界、执行原则和 reference 加载路由 |
| [references/](references/) | 按受影响行为加载的技术细则，涵盖执行、验证、语言、后端、数据库、AI/RAG 和 Git 等领域 |
| [reference-loading-test-prompts.md](reference-loading-test-prompts.md) | 用于人工回归规则路由和加载范围的提示词 |

`baseline.md` 中的 `Task-Specific References` 表是加载条件的统一入口。
assistant 根据任务影响的行为选择 reference，并只解析自身对应的路径；
无法识别 assistant 时不加载这些 task-specific references。Markdown 链接本身
不代表内容已经加载。具体优先级和授权要求以入口规则为准。

## Reference 分组

| 目录 | 内容 |
| --- | --- |
| [workflow/](references/workflow/) | 代码库发现、执行流程、验证和技术文档 |
| [git/](references/git/) | Git 工作流与 worktree 生命周期 |
| [languages/](references/languages/) | Python 与 Go |
| [backend/](references/backend/) | 后端可靠性与 API 路由设计 |
| [database/](references/database/) | 数据库访问、事务与 Schema/迁移 |
| [ai/](references/ai/) | AI 应用与 RAG 检索 |

分组只用于组织文件，不代表整组加载。加载表和 reference 内部交叉引用使用
相对于 assistant 的 `references/` 根目录的完整路径，例如
`languages/python.md` 和 `workflow/verification.md`。各文件的加载条件仍由
`baseline.md` 统一维护，不在分组内另设规则入口。

## 同步

在仓库根目录运行交互式入口，再选择 `rules` 和目标 assistant：

```bash
./sync-agents.sh
```

| 目标 | 默认根目录 | 覆盖根目录的环境变量 |
| --- | --- | --- |
| Codex | `~/.codex` | `CODEX_ROOT` |
| WorkBuddy | `~/.workbuddy` | `WORKBUDDY_ROOT` |
| OpenCode | `~/.config/opencode` | `OPENCODE_ROOT` |
| ZCode | `~/.zcode` | `ZCODE_ROOT` |
| Qoder CN | `~/.qoder-cn` | `QODER_CN_ROOT` |

同步将 `baseline.md` 覆盖写入目标根目录的 `AGENTS.md`，并将 `references/`
完整镜像到目标根目录的同名目录。目标 `references/` 中独有的文件、子目录和
隐藏文件会被删除，同名文件的本地修改也会被覆盖。需保留的自定义内容应先移出
该目录。此 README 和回归提示词文件不参与同步。

根目录环境变量只改变同步落点，不会改写 `baseline.md` 内的 reference 路径；
使用自定义路径时需同时核对实际加载路径。脚本通过 SHA-256 校验文件、
通过 `diff -qr` 校验目录；实现见 [sync-agents.sh](../sync-agents.sh)。

### 从平铺目录迁移

执行 rules 同步会配套更新 `AGENTS.md` 和嵌套的 `references/`，并清理旧平铺文件。
例如 `references/python.md` 迁为 `references/languages/python.md`，不保留旧路径副本。
分组内的文件名也去掉重复领域前缀，例如 `git/git-workflow.md` 简化为
`git/workflow.md`，`database/database.md` 改为 `database/access.md`；同步会清理旧名称。
项目规则或个人提示词中手写的旧路径也需更新；仓库同步不会修改这些外部引用。
同步后使用全新会话运行回归提示词，避免旧会话中已加载的路由影响检查。

## 维护

- 通用执行边界放在 `baseline.md`，领域细则放在对应 reference，避免重复维护。
- 新增、拆分或重命名 reference 时，同时更新入口中的加载表和受影响的引用。
- 调整加载条件后，使用回归提示词检查应加载与不应加载的场景；提示词不是自动化测试。
- 修改仓库源文件后再同步；直接编辑同步目标可能在下次同步时丢失。

同步依赖和整体使用方式见[仓库 README](../README.md)。
