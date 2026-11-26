# Skills

本目录维护可复用的任务工作流。每个 skill 的触发条件、执行步骤和授权边界由
自己的 `SKILL.md` 定义；跨任务规则见 [Rules](../rules/README.md)。

## 技能索引

| Skill | 适用场景 |
| --- | --- |
| [api-endpoint-analyzer](api-endpoint-analyzer/SKILL.md) | 分析 API 契约、调用链、业务分支、副作用和错误行为 |
| [code-changes-review](code-changes-review/SKILL.md) | 显式调用，审查 Web 前端、Python 后端及联动改动，支持当前未暂存改动、暂存区及按指定 base 审查的完整分支 |
| [code-quality-review](code-quality-review/SKILL.md) | 定向代码质量检查或开发收尾，可覆盖本次全部改动，按请求给建议或做最小等价整理 |
| [commit-helper](commit-helper/SKILL.md) | 根据 staged changes 或明确范围生成 Conventional Commit 信息，用户要求提交时执行提交流程 |
| [create-pr-or-mr](create-pr-or-mr/SKILL.md) | 根据用户指定 base 和真实 diff 起草 PR/MR 标题与描述 |
| [create-project-worktree](create-project-worktree/SKILL.md) | 基于用户选择的起始 ref 新建并附加 Codex 托管工作树，再按项目环境初始化 |
| [currrent-workspace-context](currrent-workspace-context/SKILL.md) | 只读确认工作目录、Git worktree 与分支，汇总已暂存、未暂存、未跟踪和冲突状态 |
| [rebase-as-new-branch](rebase-as-new-branch/SKILL.md) | 基于用户指定 base，在确认后通过 rebase 将分支独有提交重建到新版本分支，保留原分支 |
| [rename-worktree-chat](rename-worktree-chat/SKILL.md) | 为 Codex 主聊天标题添加工作区标识，主工作区用 `[primary]`，worktree 用路径标识，支持从侧边聊天发起 |
| [worktree-environment-setup](worktree-environment-setup/SKILL.md) | 分析 Codex 托管 worktree 初始化需求，生成或更新 .worktreeinclude，并提供 macOS 环境设置脚本 |

使用时提供任务所需的上下文，例如目标仓库、提交范围或 base ref。需要显式调用
的技能应按其 `SKILL.md` 要求指定名称；生成文案与实际提交、变更历史是不同的
执行范围。

## 目录约定

```text
skills/
├── README.md
├── targets.conf              # 限定特定技能的同步目标
├── _shared/                  # 多个 skill 共用的 reference，不是独立技能
└── <skill-name>/
    ├── SKILL.md              # 必需：名称、触发描述、核心工作流与边界
    ├── agents/openai.yaml    # 展示信息、默认 prompt 与调用策略等元数据
    ├── references/           # 可选：模板、检查清单和细则
    └── scripts/              # 可选：技能专属辅助脚本
```

共享的远端 base 解析约定见
[_shared/git-remote-base-resolution.md](_shared/git-remote-base-resolution.md)。
跨 skill 引用应保留相对目录关系，避免复制同一份约定。

## 同步

在仓库根目录运行：

```bash
./sync-agents.sh
```

依次选择 `skills`、目标 assistant、单个技能或 `all`。目标和技能菜单使用
显示的数字选择，`all` 表示所选目标支持的全部技能。支持的目标及根目录环境变量见
[Rules 的同步说明](../rules/README.md#同步)。

[同步脚本](../sync-agents.sh) 自动发现包含 `SKILL.md` 的一级目录，并依据
[`targets.conf`](targets.conf) 筛选。每行以空白分隔技能目录名和一个或多个
允许的目标 ID，支持空行和 `#` 开头的注释。未声明的技能可同步到全部目标。

每次同步先替换目标的 `skills/_shared/`，再替换选中技能的整个目录。同步范围
之外的目录由目标自行管理，包括历史安装的不兼容技能。收窄技能的目标范围后，
在受影响的目标上核对旧副本，保留所需的本地改动，再清理旧目录。

### 从旧技能名迁移

已有安装按目标同步 `all` 后，新旧目录会并存。下表中的名称同时用于
目标的 `skills/` 子目录和 `$技能名` 显式调用。

| 旧名称 | 新名称 |
| --- | --- |
| `git-code-reviewer`、`review-changes` | `code-changes-review` |
| `git-commit-helper` | `commit-helper` |
| `git-draft-pr-or-mr`、`draft-pr-or-mr` | `create-pr-or-mr` |
| `git-restack-from-base` | `rebase-as-new-branch` |
| `workspace-context` | `currrent-workspace-context` |

对每个装过旧版技能的目标，按以下顺序迁移。

1. 同步所需的新技能，核对目标中新目录的内容与仓库 `skills/<新名称>/` 一致。
2. 检查对应旧目录中是否有自行添加或修改的文件。将需要保留的内容保存到同步目录之外，或合并回维护该技能的源文件。
3. 确认所需内容已保留后，逐项删除该目标 `skills/` 下对应的旧目录。
4. 更新个人提示词、项目指令和自动化中的显式调用，例如将 `$git-code-reviewer` 改为 `$code-changes-review`。

### 清理已退役的分支创建技能

分支创建技能曾使用 `git-checkout-branch` 和 `create-branch-from-changes` 两个名称，现已退役，没有替代技能。
在每个安装过它的目标中，检查 `skills/git-checkout-branch/` 和 `skills/create-branch-from-changes/`。
先将需要保留的本地修改移到同步目录之外，再删除实际存在的旧目录，并移除个人提示词、项目指令和自动化中对这两个名称的显式调用。

## 维护

- 新增技能时保持目录名与 `SKILL.md` 中的 `name` 一致，并更新本页索引。
- 需要限制技能的同步目标时，在 `targets.conf` 声明允许的目标 ID。
- 核心工作流放在 `SKILL.md`，较长模板和检查清单放在 `references/`。
- 修改 `_shared/` 前检查所有引用它的技能，避免共同约定与各技能流程冲突。
- 更新技能后核对 frontmatter、相对链接和展示元数据；按实际变更验证示例或脚本。

项目概览与同步依赖见[仓库 README](../README.md)。
