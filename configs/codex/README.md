# Codex Config

本目录维护 Codex 的受管配置模板 [config.toml](config.toml)。具体配置值以模板
为准，通用同步入口与维护约定见 [Configs](../README.md)。

## 同步

在仓库根目录运行以下命令，再依次选择 `config` → `codex`：

```bash
./sync-agents.sh
```

默认目标为 `~/.codex/config.toml`，可通过 `CODEX_ROOT` 环境变量改变目标根目录。
此流程需要 `uv` 和 Python 3.11+；[同步脚本](../../sync-agents.sh) 使用仓库的
锁定依赖运行[合并器](../../scripts/merge_codex_config.py)。

## 受管键与本地设置

合并器使用模板中当前存在的键更新目标，保留目标中的其他键与区块。
新增模板键会开始接管目标同名键；从模板删除键不会自动删除目标中的同名键，
需要移除旧配置时应单独清理目标。

模板为 GPT-6 Sol 设置 `model_context_window = 872000`，对应 Codex 模型目录声明的
扩展上下文上限。本次更新移除了模板中的 `personality`、`features.js_repl`、
`tools.view_image` 和 `agents.job_max_runtime_seconds`，
并将 `agents.max_threads` 改为 `agents.max_concurrent_threads_per_session`。
若目标配置此前含有这些旧键，同步后需手动移除，以免旧值继续生效或与新键并存。

模板中的每个键都属于受管范围，包括 `notify`。当前 `notify` 含有本机绝对路径，
复用前应检查并调整为目标机器可用的命令，或从模板移除该键以保留目标原值。

## 备份与校验

目标已存在时，先备份到同目录的 `config.toml.backup`，仅保留最近一次同步前
的版本。写入的目标和备份权限为 `0600`；TOML 解析或合并结果校验失败时，
不覆盖原目标。

合并校验不等于 Codex 运行验证。同步后仍需在实际使用环境中确认相关配置、
通知命令和外部服务可用。
