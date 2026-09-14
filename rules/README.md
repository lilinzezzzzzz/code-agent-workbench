# Rules

本目录维护跨项目的 agent 行为基线和按需加载的技术规则。任务专属流程见
[Skills](../skills/README.md)，assistant 运行配置见
[Configs](../configs/README.md)。

## 内容与加载方式

| 路径 | 用途 |
| --- | --- |
| [agents.md](agents.md) | always-on 入口：指令优先级、授权边界、执行原则和 reference 加载路由 |
| [references/](references/) | 按受影响行为加载的技术细则，涵盖执行、验证、语言、后端、数据库、AI/RAG 和 Git 等领域 |
| [reference-loading-test-prompts.md](reference-loading-test-prompts.md) | 用于人工回归规则路由和加载范围的提示词 |

`agents.md` 中的 `Task-Specific References` 表是加载条件的统一入口。
assistant 根据任务影响的行为选择 reference，并只解析自身对应的路径；
无法识别 assistant 时不加载这些 task-specific references。Markdown 链接本身
不代表内容已经加载。具体优先级和授权要求以入口规则为准。

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

同步将 `agents.md` 覆盖写入目标根目录的 `AGENTS.md`，并将 `references/`
完整镜像到目标根目录的同名目录。目标 `references/` 中独有的文件、子目录和
隐藏文件会被删除，同名文件的本地修改也会被覆盖。需保留的自定义内容应先移出
该目录。此 README 和回归提示词文件不参与同步。

根目录环境变量只改变同步落点，不会改写 `agents.md` 内的 reference 路径；
使用自定义路径时需同时核对实际加载路径。脚本通过 SHA-256 校验文件、
通过 `diff -qr` 校验目录；实现见 [sync-agents.sh](../sync-agents.sh)。

## 维护

- 通用执行边界放在 `agents.md`，领域细则放在对应 reference，避免重复维护。
- 新增、拆分或重命名 reference 时，同时更新入口中的加载表和受影响的引用。
- 调整加载条件后，使用回归提示词检查应加载与不应加载的场景；提示词不是自动化测试。
- 修改仓库源文件后再同步；直接编辑同步目标可能在下次同步时丢失。

同步依赖和整体使用方式见[仓库 README](../README.md)。
