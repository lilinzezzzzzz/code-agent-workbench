# Configs

本目录保存各 assistant 的配置源文件。行为规则见 [Rules](../rules/README.md)，
任务工作流见 [Skills](../skills/README.md)；配置同步与这两类内容分别选择。

## 配置索引

| Assistant | 源文件 | 默认目标 | 同步方式 |
| --- | --- | --- | --- |
| [Codex](codex/README.md) | [codex/config.toml](codex/config.toml) | `~/.codex/config.toml` | 按模板中的受管键合并 |
| [OpenCode](opencode/README.md) | [opencode/opencode.jsonc](opencode/opencode.jsonc) | `~/.config/opencode/opencode.jsonc` | 整个文件覆盖 |

具体配置值以源文件为准，合并边界、备份行为和环境准备见各 assistant 的 README。
当前同步入口只提供这两个 assistant 的 config 选项；rules 和 skills 的目标列表更广。

## 同步

在仓库根目录执行，再依次选择 `config` 和目标 assistant：

```bash
./sync-agents.sh
```

使用 `CODEX_ROOT` 或 `OPENCODE_ROOT` 环境变量可以改变对应目标根目录。
入口为交互式脚本，不接受命令行参数。通用依赖见
[仓库 README](../README.md)，实现见 [sync-agents.sh](../sync-agents.sh)。

## 维护

- 只提交可复用的配置，不添加 API Key、token、cookie 等凭据；机器路径需明确其适用范围。
- 调整配置前检查对应 assistant 的同步边界，确认哪些本地设置会被保留或覆盖。
- 新增 assistant 配置目录不会自动增加 config 菜单项，还需更新同步入口、对应测试和本页索引。
- 配置内容、复制或合并校验与 assistant 运行验证是不同层次；同步成功不代表插件、模型或外部服务已可用。
