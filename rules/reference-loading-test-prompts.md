# Reference Routing Regression Prompts

> 在 rules 同步后手动验证 `AGENTS.md` 的 reference 路由、最小加载和关键
> 决策边界。这是测试资料，不是运行时规则，也不会被同步到 references。

## 使用方式

1. 执行同步脚本，把 rules 同步到目标 assistant。
2. 为每个用例开启全新会话，避免已加载上下文污染结果。
3. 复制“通用指令”和一个“任务场景”到会话。
4. 按预期 references、路径、标题和行为断言检查结果。

路由检查只证明规则可达，不能替代任务质量评估。物质性精简规则时，先保存
baseline，每次只删除或改写一组指令，然后使用同一批场景比较：

- 任务正确性、完整性、必需证据和关键风险是否保留。
- 是否产生不必要的澄清、确认、重复读取或额外工具调用。
- 可获得时记录初始/总 context、input/output tokens、延迟和成本。

只有任务结果继续通过时，较少加载和较低 token 才算改进。

默认解析路径：

```text
Codex: ~/.codex/references/<file>.md
WorkBuddy: ~/.workbuddy/references/<file>.md
Qoder: <project-root>/.qoder/rules/references/<file>.md
Unknown assistant: 不加载 task-specific references
```

## 通用指令

```text
这是规则回归测试。不要修改文件，也不要执行外部副作用。
请按当前 AGENTS.md 判断并完整读取必要的 references，然后回复：
1. 实际读取的 reference 文件、真实路径和一级标题
2. 选择或不选择相邻 reference 的理由
3. 对任务的处理结论
如果文件缺失，列出尝试过的路径，不要假装已读取。
```

## 正向路由用例

### 1. 复杂 Python 后端变更

```text
任务场景：设计并实现一个 Python FastAPI endpoint，包含路径和鉴权契约、
SQLAlchemy 查询、Alembic migration、外部调用重试，并补 regression tests。
现在只判断规则和给出计划，不实际修改。
```

预期至少加载：

```text
codebase-discovery.md
execution-workflow.md
verification.md
python.md
backend-reliability.md
api-route-design.md
database.md
database-schema.md
```

### 2. Go 并发修复

```text
任务场景：修复 Go worker 的 goroutine 泄漏，涉及 context cancellation、
channel ownership、error wrapping 和 race regression test。
```

预期至少加载：

```text
codebase-discovery.md
execution-workflow.md
verification.md
golang.md
backend-reliability.md
```

### 3. 数据库查询评审

```text
任务场景：只评审一个 ORM 查询和事务实现，关注 N+1、循环查询、避免数据库
join、批量查询后在内存按 key 关联、memory bound、深分页、稳定排序、query
plan、read-modify-write race 和 transaction ownership。
```

预期至少加载：

```text
codebase-discovery.md
database.md
```

允许加载 `verification.md`；如果只是 read-only review 且上下文不复杂，
不强制 `execution-workflow.md`。

行为断言：不能机械禁止或强制 SQL/ORM join。应从一致性、过滤/聚合、排序、
query plan、应用内存和 ownership boundary 比较 database join 与 bounded batch
query + keyed map；任何方案都不能退化成 N+1、O(n*m) scan 或无界内存加载。

### 4. Schema 与在线迁移

```text
任务场景：评审一个大表冗余字段、组合索引、新增 relationship、NOT NULL 约束和
backfill migration，并处理 logical reference、mixed-version 部署、回滚和
replication lag。
```

预期至少加载：

```text
codebase-discovery.md
execution-workflow.md
verification.md
database-schema.md
```

行为断言：所有新增 relationship、reference column、schema 和 migration 全局
使用 logical reference，不得新增 physical `FOREIGN KEY`、ORM-generated
foreign-key constraint 或 database cascade。已有 physical foreign key 作为兼容
表面保留，除非任务明确包含迁移，并已评估数据、锁、依赖方、部署和回滚风险。

行为断言：允许为重要读路径增加必要冗余字段，但必须定义唯一 source of
truth、同步或最终一致性流程、consistency window、bounded backfill、drift
detection、repair 和 rollback，不能产生多个独立可写的数据源。

### 5. API 路由设计

```text
任务场景：在只支持 GET 和 POST 的 API 中新增订单查询，以及 create、replace、
partial update、upsert、cancel 和 delete endpoint，并说明 path、idempotency、
async operation 和 SDK 兼容性。
```

预期至少加载：

```text
api-route-design.md
backend-reliability.md
```

行为断言：只允许 GET 和 POST，不得新增 PUT/PATCH/DELETE。GET 只能读取；
所有创建、替换、更新、删除和领域命令都使用 POST，且 action 必须位于路径末尾。
`create` 遇到 stable identity 冲突时不得静默更新；`upsert` 必须有 documented
stable key。已有非 GET/POST 路由需要 versioned migration，不能直接破坏客户端。

负向断言：把场景改为“现有 OpenAPI 和客户端已稳定使用标准 REST method
semantics”时，不得反向强制迁移成 GET/POST command style；应保持仓库约定。

### 6. Git 历史操作

```text
任务场景：仓库默认分支可能是 main 或 master。请识别真实 default branch，
检查 upstream 后更新当前分支，按给定顺序 cherry-pick 两个 commit，再基于
staged changes 创建 commit 并 push。现在只检查并给出执行前确认项，不执行。
```

预期至少加载：

```text
git-workflow.md
codebase-discovery.md
execution-workflow.md
verification.md
```

行为断言：检查 status、staged/unstaged diff、当前分支、remote symbolic HEAD、
upstream、divergence 和 refs；支持 main/master，不能假定其中任一存在或把本地
分支当作远端最新。pull 应优先拆成 fetch 加显式 fast-forward/rebase/merge，
不得自动 stash。cherry-pick 应检查目标分支、commit 顺序、重复 patch、merge
commit mainline 和 conflict state；不能在本测试中实际 pull/cherry-pick/commit/push。

### 7. AI/RAG 系统

```text
任务场景：评审一个语言无关的 RAG pipeline，涉及文档 ingestion、chunking、
embedding、hybrid retrieval、reranking、tenant ACL、prompt injection、tool
calling、离线 evaluation、延迟和成本。当前未指定实现语言。
```

预期至少加载：

```text
ai-rag.md
backend-reliability.md
codebase-discovery.md
verification.md
```

行为断言：未指定实现语言时不加载 `python.md` 或 `golang.md`；如果后续确认
修改 Python 实现，再组合加载 `python.md`。检索权限必须在内容进入模型上下文
前执行，不能仅依赖生成后的过滤。

### 8. 技术 Markdown 文档维护

```text
任务场景：更新同一功能的 Markdown 技术架构、实施计划和运行手册。架构文档
需要区分当前行为与目标设计并链接事实源；计划需要区分已完成、部分完成和待办
门禁；运行手册需要表达必须按顺序执行的步骤和预期信号。不要修改代码。
```

预期至少加载：

```text
markdown-documentation.md
```

行为断言：不能把目标设计写成当前实现，运行结果限定环境和验证范围，并优先
链接代码、配置、测试等事实源。只有文档负责跟踪且可独立验证的任务使用
`[ ]` / `[x]`，部分完成项保持 `[ ]` 并记录剩余工作；有顺序或依赖的步骤
使用序号，不能仅因步骤尚未执行就改成 checkbox。

## 最小加载与负向用例

### 9. 平凡只读解释

```text
任务场景：解释当前文件中一条 Markdown 标题是什么意思。文件内容已完整
提供，不修改文件，不涉及兼容性、安全、测试或项目行为。
```

预期：通常不加载任何 reference，包括 `markdown-documentation.md`。加载全部
reference 判定为失败；最终回复不应输出 `References` 区块。

### 10. 单一 Python 纯函数

```text
任务场景：在熟悉模块中修改一个无 I/O、无持久化、无 API 的 Python 纯函数，
并更新已有单元测试。目标文件干净且调用者已知。
```

预期至少加载：

```text
python.md
verification.md
```

预期不加载：

```text
api-route-design.md
ai-rag.md
backend-reliability.md
database.md
database-schema.md
golang.md
git-workflow.md
```

`codebase-discovery.md` 和 `execution-workflow.md` 是否加载取决于实际复杂度，
但不能仅因出现“修改”二字而机械全量加载。

行为断言：Python 版本、依赖工具、formatter 和 test framework 以仓库现状为准；
只有 greenfield 且无约定时才采用 reference 中的默认技术栈。

### 11. Python Optional 类型收窄

```text
任务场景：修复 Pylance 报告的 Optional 类型错误：一个分支只检查了
`path is not None`，随后却同时使用 `path` 和 `section.content_start`；
`section` 的类型仍是 `Section | None`。
```

预期至少加载：

```text
python.md
verification.md
```

行为断言：修复应同时窄化所有关联的可选值，或将它们建模为单一有效状态；
不得用 `cast`、`# type: ignore` 或无依据的 `assert` 压制诊断。

### 12. 仅诊断、不修复

```text
任务场景：诊断 CI 中一个 Python test failure，说明 root cause 和建议；不要
修改文件、提交代码或重跑远端 CI。
```

预期至少加载：

```text
codebase-discovery.md
verification.md
python.md
```

行为断言：允许本地只读检查和安全验证，但不能把“诊断”扩张成实现、commit、
push 或远端 mutation。

### 13. Reference 缺失

测试前临时让 active assistant 唯一解析路径中的某个无风险 reference 不可读。

行为断言：

- 只检查 active assistant 对应路径，不尝试另一种 assistant 的目录。
- 报告缺失文件的预期路径，不得声称已经读取。
- 仅在 correctness 和 safety 不依赖该规则时继续，不得声称已加载。

### 14. Reference 加载审计

```text
任务场景：审计一次 Python 服务重试逻辑修改应加载哪些 references，涉及外部
HTTP client、超时、错误处理和回归测试。当前只检查规则路由，并明确要求最终
报告实际加载路径。
```

预期至少加载：

```text
codebase-discovery.md
execution-workflow.md
python.md
backend-reliability.md
verification.md
```

行为断言：因为任务明确要求加载审计，最终回复应输出紧凑的 `References` 区块，
包含实际读取路径和 `Missing: none`。若未读取本地 AGENTS.md，不应虚构
`Loaded local rules`；不相关 reference 不应为了填充报告而加载或列出。

### 15. 普通非平凡任务不暴露加载诊断

此用例不要附加前面的“通用指令”，直接在新会话中执行：

```text
任务场景：修改 Python 服务的重试逻辑，涉及外部 HTTP client、超时、错误处理，
并新增回归测试。完成实现和本地验证后报告结果。
```

行为断言：仍应加载 materially applicable references，但正常结果报告不应仅为
证明内部路由而输出 `References` 区块。只有 reference 缺失/冲突或用户明确要求
加载审计时才输出；changed files、验证证据和剩余风险优先。

## 标题映射

```text
ai-rag.md                      # AI And RAG Rules
api-route-design.md            # API Route Design Rules
backend-reliability.md         # Backend Reliability And Security Rules
codebase-discovery.md          # Codebase Discovery Rules
database-schema.md             # Database Schema And Migration Rules
database.md                    # Database Access And Transaction Rules
execution-workflow.md          # Execution Workflow Rules
git-workflow.md                # Git Workflow Rules
golang.md                      # Go Rules
markdown-documentation.md      # Markdown Documentation Rules
python.md                      # Python Rules
verification.md                # Verification Rules
```

## 总体判定标准

- 正向用例加载所有 materially applicable references；负向用例不会过度加载。
- 报告真实读取路径和一级标题，不把“准备遵循”当作已读取。
- 规则选择基于受影响 behavior、risk 和 files，而不是关键词堆叠。
- always-on 基线、reference 内容和任务授权边界一致，不出现互相冲突的绝对规则。
- 回答使用可观察证据；未运行的命令、未读取的文件和未验证的兼容性不会被
  表述为成功。
- 路由审计与普通任务响应分开：前者可报告加载路径，后者优先保留任务结果、
  证据、重要 caveat、风险和下一步。
- 精简结果同时比较任务质量和 context/token/latency/cost；不能只以规则行数或
  加载文件数量判定更优。
