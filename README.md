# Code Agent Workbench

> 个人 AI assistant rules、skills 与同步工具，支持 Codex、Qoder 和
> AGENTS.md 工作流，聚焦渐进式披露与 harness engineering

一套可复用的个人级 AI assistant 配置工作台，包含编码规范、Git 工作流、
AGENTS 指令、按需加载的 references 与 skills。同一份内容可以服务于
Codex、Qoder 以及其他支持类似机制的开发工具，用 rules 驱动可维护的
assistant harness。

---

## 📋 目录结构

```text
code-agent-workbench/
├── .github/
│   └── rulesets/             # GitHub repository ruleset exports
├── pyproject.toml             # uv 项目与 Python 版本约束
├── uv.lock                    # uv 锁文件
├── sync-agents.sh            # 统一同步入口：rules / skills / Codex config
├── configs/
│   └── codex-config.toml     # Codex config 受管键模板
├── scripts/
│   └── merge_codex_config.py # 保留本机设置的 TOML 合并器
├── tests/
│   └── test_merge_codex_config.py  # Codex config 合并与入口测试
├── rules/                    # 规则源文件；Codex 同步时生成 AGENTS.md
│   ├── agents.md             # 同步到 Codex 根目录 AGENTS.md 的源模板
│   ├── reference-loading-test-prompts.md  # references 加载验证提示词
│   └── references/
│       ├── ai-rag.md                # AI 应用、RAG、评估、安全与成本规则
│       ├── api-route-design.md      # GET 资源路径与 POST 命令路径规则
│       ├── backend-reliability.md  # 后端可靠性、安全、API/worker 规则
│       ├── codebase-discovery.md   # 代码库上下文发现与影响面规则
│       ├── database.md             # 数据库查询、事务与并发规则
│       ├── database-schema.md      # Schema、冗余字段、索引、逻辑外键与迁移规则
│       ├── execution-workflow.md   # 非平凡任务执行流程规则
│       ├── git-workflow.md         # Git 安全工作流规则
│       ├── golang.md               # Go 语言与标准工具链规则
│       ├── project-agents-maintenance.md  # 项目级 AGENTS.md 维护规则
│       ├── python.md               # Python 规则
│       └── verification.md         # 测试与验证规则
├── agents/                   # Agent 配置文件（预留）
├── events/                   # 事件处理配置（预留）
├── skills/
│   ├── api-endpoint-analyzer/
│   ├── git-code-reviewer/
│   ├── git-commit-helper/
│   ├── git-draft-pr-or-mr/
│   └── git-restack-from-base/
└── README.md
```

---

## 🎯 核心组件

### rules/

规则源文件。同步 Codex 时，`rules/agents.md` 只会写入 Codex 根目录的
`AGENTS.md`，`rules/references/` 下的规则文件会同步到 Codex 根目录的
`references/`，供渐进式披露读取。当前 references 覆盖执行流程、
代码库发现、Git 工作流、Python、Go、AI/RAG、API 路由设计、后端可靠性、
数据库访问、Schema/迁移、Agent 指令维护、测试验证等高频技术场景。
同步 Qoder 时，脚本会
要求输入项目 `.qoder` 目录，并把 `agents.md` 和 `rules/references/`
下的规则文件增量同步到该目录下的 `rules/`：

- **适用范围**: Codex 和其他支持 `AGENTS.md` 规则注入的工具
- **角色定位**: 跨项目安全基线、执行边界和渐进式规则路由
- **项目优先**: 项目内约定优先于全局技术偏好，避免跨仓库机械套用
- **规则质量**: 强规则必须有明确作用域、触发条件和可验证结果
- **Git 规范**: 保护用户工作区和历史，仓库约定优先
- **渐进式披露**: 执行流程、代码库发现、Git、Python、Go、AI/RAG、
  API 路由设计、后端可靠性、数据库访问、Schema/迁移、Agent 指令维护和验证细则
  下沉到 `rules/references/`，同步到 Codex 后位于
  `~/.codex/references/`。
  `AGENTS.md` 会集中定义 reference search paths：Codex 只解析
  `~/.codex/references/`，Qoder 解析项目 `.qoder/rules/references/`；无法
  识别 active assistant 时不加载 task-specific references，也不依赖
  Markdown 链接自动展开
- **Harness engineering**: 把 always-on 基线、按需 references、skills
  和同步脚本拆成可演进的 assistant runtime 配置，避免把长期规则散落在
  单次 prompt 中

### Skills 与同步脚本

当前目录已经包含一组可复用能力：

- **sync-agents.sh**: 统一同步入口，可交互选择 `rules` 或单个
  `skill`；同步 rules 到 Codex 时写入 `AGENTS.md` 和顶层
  `references/`，同步 rules 到 Qoder 时写入指定项目 rules 目录；同步
  Codex config 时只覆盖模板管理的键，并保留本机专属配置
- **api-endpoint-analyzer**: 系统化分析 API endpoint 的请求、响应、业务流程与错误处理
- **git-code-reviewer**: 基于 diff 输出高信号代码审查结论，优先发现 bug、回归和风险
- **git-commit-helper**: 基于 staged diff 生成或执行规范的 Conventional Commit
- **git-draft-pr-or-mr**: 基于明确 base ref 和真实 git diff 生成精简的 PR/MR 标题与描述
- **git-restack-from-base**: 基于显式基础分支重新切出版本化分支，并按原顺序 cherry-pick 当前分支独有提交

### 扩展模块（预留）

- **agents/**: 个人 Agent 行为定制
- **events/**: 个人工作流事件处理
- **skills/**: 个人专业技能模块

### GitHub rulesets

`.github/rulesets/` 保存 GitHub repository ruleset 导出文件，便于在新仓库中手动导入或通过 GitHub API 同步。当前维护的 `Git-Flow-Branch-Naming.json`
会保护 `main` 和 `dev`，禁止删除和 non-fast-forward 更新，并要求通过 pull request 修改。

### Skill 目录约定

当前 `skills/` 目录采用统一结构，便于同步、复用和持续演进：

```text
skills/<skill-name>/
├── SKILL.md                  # 触发描述、核心工作流、边界规则
├── agents/
│   └── openai.yaml           # UI 展示名、短描述、默认 prompt
├── references/               # 按需加载的模板、检查清单、选择规则
└── scripts/                  # 可选，本地辅助脚本或命令封装
```

设计原则：

- `SKILL.md` 保持精简，只放高价值流程和决策规则
- 细节模板、checklist、示例下沉到 `references/`
- `agents/openai.yaml` 负责展示层和默认触发入口
- `scripts/` 只放 skill 专属、值得复用的执行逻辑，避免把复杂 shell
  直接塞进说明文档
- skill 命名与目录名保持一致，避免同步或调用时混淆
- `sync-agents.sh` 会自动发现包含 `SKILL.md` 的一级 skill 目录，
  无需手动维护 skill 列表

---

## 🚀 快速开始

### 1. 应用个人配置

执行统一同步脚本后，按提示选择要同步的内容类型。选择 `skills` 时，
脚本会继续要求选择目标 assistant：

```bash
./sync-agents.sh
```

**脚本功能说明**:

- **内容选择**: 支持 `rules`、`skills`、`codex-config`
- **config 流程**: 将 `configs/codex-config.toml` 中出现的受管键合并到
  Codex 根目录的 `config.toml`，目标中的其他键和区块保持原样
- **config 受管边界**: 每次以模板中当前存在的键为受管键；从模板删除键不会
  自动删除目标中的同名键，需要时应在目标配置中显式清理
- **config 备份**: 目标存在时先备份为 `config.toml.backup`；目标和备份
  都保持 `0600` 权限。备份保留最近一次同步前的版本；合并或 TOML 校验
  失败时不覆盖原文件
- **rules 流程**: 先选择 `codex` 或 `qoder`；选择 `qoder` 时必须输入
  以 `.qoder` 结尾的目标项目目录，例如 `/path/to/project/.qoder`
- **skills 流程**: 先选择具体 skill 或全部 skills，再选择目标 assistant
- **目标选择**: rules 支持 `codex` 或 `qoder`；`skills` 支持 `codex`、
  `qoder` 或 `both`
- **覆盖策略**: Codex config 按受管键合并；`AGENTS.md` 直接覆盖；顶层
  `references/` 和 `skills/` 仅覆盖同名项
- **完整性校验**: Codex config 使用 TOML 解析和合并结果校验；其他文件使用
  SHA-256，目录使用 `diff -qr`
- **依赖要求**: 需要 `diff`；`codex-config` 流程额外需要 `uv` 和 Python
  3.11+。`uv` 根据项目 `pyproject.toml` 创建或复用虚拟环境；文件校验会
  优先使用 `sha256sum`，并兼容 `shasum` 或 `openssl`

### 2. 典型用法

- 选择 `rules` -> `codex`：把 `rules/agents.md` 同步为 Codex 根目录的
  `AGENTS.md`，并把 `rules/references/` 下的源规则同步到 `references/`
- 选择 `rules` -> `qoder`：输入以 `.qoder` 结尾的项目目录，并把
  `agents.md` 和 `rules/references/` 下的规则文件同步到该目录下的
  `rules/`
- 选择 `codex-config`：把 `configs/codex-config.toml` 中的受管键合并到
  Codex 根目录的 `config.toml`，同时备份原文件并保留本机专属配置
- 选择 `skills`：选择一个 skill 或全部 skills，并同步到目标 assistant 的 `skills/`
- skills 选择 `both`：将选中的 skill 同步到当前配置的所有目标目录

当前已维护的 skill 更适合以下场景：

- `api-endpoint-analyzer`：解释接口契约、梳理调用链、核对实现与文档是否一致
- `git-code-reviewer`：审查 PR、MR、commit 或 diff，输出带 severity 的
  具体 findings
- `git-commit-helper`：根据 staged changes 生成 commit message，或在范围清晰时执行提交
- `git-draft-pr-or-mr`：基于显式 base branch 或 base ref，生成可直接
  粘贴到 GitHub/GitLab 的 PR/MR 文案
- `git-restack-from-base`：把当前功能分支基于新 base 重建为 `-v2`、
  `-v3` 等版本化分支，并在确认后执行 cherry-pick

### 3. 个性化定制

根据个人喜好和技术栈，在预留目录中添加：

- 个人偏好的 Agent 行为规则
- 符合个人工作流的事件处理
- 专业领域的个人技能模块
- 遵循
  `SKILL.md + agents/openai.yaml + optional references/ + optional scripts/`
  的 skill 结构

---

## 📋 开发规范摘要

### 编程语言规范

**Python 开发**:

- 使用 Python 3.11+、`uv`、`pyproject.toml` 和 Ruff/Pylance-compatible typing；
  对关联 Optional 状态显式窄化
- 后端使用 FastAPI、Pydantic v2、SQLAlchemy 2.x 和 Alembic
- 异步并发与 HTTP 使用 AnyIO 和 HTTPX，保留 cancellation 与 bounded concurrency
- 测试使用 pytest，并通过 `uv run` 执行项目工具

**Golang 开发**:

- 遵循项目声明的 Go 版本、module、生成和验证命令
- 优先标准库和现有依赖，避免无关 module churn
- 显式处理 error、context、资源 ownership 和 cancellation
- 每个 goroutine 都有 owner、边界和终止路径

### Git 工作流

**分支命名**:

优先遵循仓库约定；无约定时使用语义前缀：

- `feature/<description>`
- `bugfix/<description>`
- `hotfix/<description>`
- `release/<version>`

**提交信息格式**:

```text
<type>(<scope>): <subject>

[optional body]
```

**提交类型**:

- `feat`: 新功能
- `fix`: 修复 bug
- `chore`: 构建过程或辅助工具变动
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构代码
- `test`: 测试相关
- `perf`: 性能优化
- `ci`: CI/CD 配置变更

---

## 🛠️ 使用建议

### 个人优化

1. 根据个人编码习惯调整规范细节
2. 定期回顾和优化个人工作流
3. 持续完善个人技能库

### 项目适配

1. 针对不同项目类型调整配置重点
2. 在 `skills/` 或预留目录中建立项目模板
3. 积累个人最佳实践案例

### 持续进化

1. 跟踪个人技术成长轨迹
2. 学习并整合新的开发方法
3. 定期重构个人配置体系

---

## 📚 相关资源

- [Conventional Commits 规范](https://www.conventionalcommits.org/)
- [Python 官方文档](https://docs.python.org/)
- [Go 编程语言规范](https://golang.org/doc/effective_go)
- 对应 assistant 或 IDE 的官方文档

---

## 📄 许可证

本配置集采用 MIT 许可证，可根据需要自由修改和分发。

---

## 🤝 个人维护

建议 Fork 此配置作为个人开发环境的基础，根据自己的需求进行定制化改进！

**适用对象**: 独立开发者、技术爱好者
**核心价值**: 个人编码效率提升、AI 辅助开发体验优化
