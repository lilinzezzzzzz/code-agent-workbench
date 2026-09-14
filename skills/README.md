# Skills

本目录维护可复用的任务工作流。每个 skill 的触发条件、执行步骤和授权边界由
自己的 `SKILL.md` 定义；跨任务规则见 [Rules](../rules/README.md)。

## 技能索引

| Skill | 适用场景 |
| --- | --- |
| [api-endpoint-analyzer](api-endpoint-analyzer/SKILL.md) | 分析 API 契约、调用链、业务分支、副作用和错误行为 |
| [git-checkout-branch](git-checkout-branch/SKILL.md) | 根据当前修改推荐分支名，并按技能约定确认后从当前 HEAD 切出新分支 |
| [git-code-reviewer](git-code-reviewer/SKILL.md) | 显式调用，基于用户指定 base 审查当前 Python 后端分支的完整已提交差异 |
| [git-commit-helper](git-commit-helper/SKILL.md) | 根据 staged changes 或明确范围生成 Conventional Commit 信息，用户要求提交时执行提交流程 |
| [git-create-worktree](git-create-worktree/SKILL.md) | 创建或复用任务 worktree，明确分支、路径与 base |
| [git-draft-pr-or-mr](git-draft-pr-or-mr/SKILL.md) | 根据用户指定 base 和真实 diff 起草 PR/MR 标题与描述 |
| [git-restack-from-base](git-restack-from-base/SKILL.md) | 基于用户指定 base，在确认后通过 rebase 将分支独有提交重建到新版本分支，保留原分支 |

使用时提供任务所需的上下文，例如目标仓库、提交范围或 base ref。需要显式调用
的技能应按其 `SKILL.md` 要求指定名称；生成文案与实际提交、变更历史是不同的
执行范围。

## 目录约定

```text
skills/
├── README.md
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

依次选择 `skills`、单个技能或 `all`、目标 assistant。技能和目标菜单使用
显示的数字选择。支持的目标及根目录环境变量见
[Rules 的同步说明](../rules/README.md#同步)。

[同步脚本](../sync-agents.sh) 自动发现包含 `SKILL.md` 的一级目录，
新增技能无需手动更新脚本列表。每次同步都会先替换目标的 `skills/_shared/`，
再替换选中技能的整个目录，包括清理这些目录中的目标独有文件和本地修改。
未选中的技能及其他目标技能目录保留；`all` 也不会删除仓库中已不存在的旧技能。
本 README 不会作为技能同步。

## 维护

- 新增技能时保持目录名与 `SKILL.md` 中的 `name` 一致，并更新本页索引。
- 核心工作流放在 `SKILL.md`，较长模板和检查清单放在 `references/`。
- 修改 `_shared/` 前检查所有引用它的技能，避免共同约定与各技能流程冲突。
- 更新技能后核对 frontmatter、相对链接和展示元数据；按实际变更验证示例或脚本。

项目概览与同步依赖见[仓库 README](../README.md)。
