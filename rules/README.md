# Rules

本目录维护适用于所有任务的通用协作原则，以及仅适用于技术工作的工程规则。
非技术任务仍遵循独立判断、授权和证据要求，普通对话保持自然、轻量，
不套用工程流程。任务专属流程见
[Skills](../skills/README.md)，assistant 运行配置见
[Configs](../configs/README.md)。

`baseline.md` 是仓库中的源文件名；同步后使用各 assistant 识别的 `AGENTS.md`
作为目标文件名。两者内容一致，维护时修改源文件后再同步。

## 内容与加载方式

| 路径 | 用途 |
| --- | --- |
| [baseline.md](baseline.md) | always-on 入口：通用协作原则、限定技术范围的工程规则和 reference 加载路由 |
| [references/](references/) | 仅用于工程任务的按需细则，涵盖执行、验证、语言、后端、数据库、AI/RAG 和 Git 等领域 |
| [reference-loading-test-prompts.md](reference-loading-test-prompts.md) | 用于人工回归规则路由、加载范围和执行行为的提示词 |

`baseline.md` 分为 `General Collaboration` 和 `Engineering Work` 两层。
前者适用于所有任务，后者只适用于代码、软件系统、基础设施、技术配置和
工程文档等工作。混合任务只对技术部分应用工程规则；例如编写数据处理脚本
按工程规则验证，业务结论按通用证据原则审查，不将整份分析变成代码评审。

`Engineering Work` 中的 `Task-Specific References` 表是加载条件的统一入口。
assistant 先判断当前任务部分是否属于工程范围，再按受影响行为选择 reference。
解析基准为声明这段加载规则的入口 `AGENTS.md` 同级的 `references/`，不按
assistant 名称选择目录。入口来源路径必须由加载上下文或已核实的文件证据确定；
无法确定时报告基准未确认，只继续不依赖这些 references 的工作，不猜测默认路径。
Markdown 链接本身不代表内容已经加载。具体优先级和授权要求以入口规则为准。

`workflow/` 也属于工程 references；普通文稿、生活规划、业务分析不会仅因
涉及多个文件、风险、验证、Markdown 格式或外部工具就触发这些规则。
适用的其他 skills 和工具指令仍按自身范围执行，不自动触发工程 references。

入口规则被注入上下文，不等于其中每一部分都适用于当前任务。话题切换后，
先前读过的 reference 可能仍在上下文中，但超出当前任务范围时不应继续应用。

## Reference 分组

| 目录 | 内容 |
| --- | --- |
| [workflow/](references/workflow/) | 代码库发现、执行流程、验证和技术文档 |
| [git/](references/git/) | 当前工作目录中的 Git 操作、分支、历史与远端安全 |
| [languages/](references/languages/) | Python 与 Go |
| [backend/](references/backend/) | 后端可靠性与 API 路由设计 |
| [database/](references/database/) | 数据库访问、事务与 Schema/迁移 |
| [ai/](references/ai/) | AI 应用与 RAG 检索 |

分组只用于组织文件，不代表整组加载。加载表和 reference 内部交叉引用使用
相对于声明规则的入口文件同级 `references/` 根目录的完整路径，例如
`languages/python.md` 和 `workflow/verification.md`。各文件的加载条件仍由
`baseline.md` 统一维护，不在分组内另设规则入口。

从子目录执行命令、读取嵌套 reference 或加载另一个项目级 `AGENTS.md`，都不
改变原入口的解析基准；另一个入口若声明自己的 references，则使用它自己的基准。
仓库维护时源入口名为 `rules/baseline.md`，对应源文件位于同级 `rules/references/`；
同步后入口名为 `AGENTS.md`，两者保持相同的目录关系。

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
| DeepSeek Harness | `~/.dsh` | 不支持覆盖 |

同步将 `baseline.md` 覆盖写入目标根目录的 `AGENTS.md`，并将 `references/`
完整镜像到目标根目录的同名目录。目标 `references/` 中独有的文件、子目录和
隐藏文件会被删除，同名文件的本地修改也会被覆盖。需保留的自定义内容应先移出
该目录。此 README 和回归提示词文件不参与同步。

根目录环境变量改变同步落点；references 随已确认的入口位置解析，无需改写
规则中的路径。使用自定义根目录时仍须让 agent 能确认实际加载的 `AGENTS.md`
来源，不能只注入不带来源的文本并假定它知道所在目录。脚本通过 SHA-256 校验文件、
通过 `diff -qr` 校验目录；实现见 [sync-agents.sh](../sync-agents.sh)。

DeepSeek Harness 默认安装时只会自动加载用户全局的 `~/.dsh/AGENTS.md`（即同步目标
文件本身）；`references/` 与 `skills/` 不会被自动注入，而是由 agent 在执行
任务时按 `baseline.md` 的路由和 `SKILL.md` 的触发条件按需读取。因此该目标
必须保证 `~/.dsh/references/` 真实存在，且 session 有读取该目录的权限。

### 从平铺目录迁移

执行 rules 同步会配套更新 `AGENTS.md` 和嵌套的 `references/`，并清理旧平铺文件。
例如 `references/python.md` 迁为 `references/languages/python.md`，不保留旧路径副本。
分组内的文件名也去掉重复领域前缀，例如 `git/git-workflow.md` 简化为
`git/workflow.md`，`database/database.md` 改为 `database/access.md`；同步会清理旧名称。
项目规则或个人提示词中手写的旧路径也需更新；仓库同步不会修改这些外部引用。
同步后使用全新会话运行回归提示词，避免旧会话中已加载的路由影响检查。

## 维护

- 通用协作原则放在 `baseline.md` 的 `General Collaboration`，工程约束和路由
  放在 `Engineering Work`，工程领域细则放在对应 reference，避免重复维护。
- 独立判断与方案审查由 `baseline.md` 的 `Independent Judgment And Proposal Review`
  统一定义，适用于技术与非技术任务；审查用户及 agent 自身的方案，同时保留
  明确约束、授权边界和持续执行要求，不为普通对话增加形式化审查。
- 新增、拆分或重命名 reference 时，同时更新入口中的加载表和受影响的引用。
- 调整加载条件后，使用回归提示词检查应加载与不应加载的场景；提示词不是自动化测试。
- 调整适用范围后，检查非技术任务、混合任务和话题切换；不能将“不加载工程
  references”理解为不需要通用独立判断、授权边界或证据核对。
- 调整决策或执行规则后，补充相应行为回归，同时检查必要异议与过度质疑；
  静态检查不能证明模型实际遵循规则，未运行的会话用例应标为未验证。
- 修改仓库源文件后再同步；直接编辑同步目标可能在下次同步时丢失。

同步依赖和整体使用方式见[仓库 README](../README.md)。
