# OpenCode Config

本目录维护可复用的 OpenCode 配置 [opencode.jsonc](opencode.jsonc)。通用同步入口
与维护约定见 [Configs](../README.md)。

后续新增配置时，请勿提交 API Key、token、cookie、真实服务凭证或其他机器私有信息。

## 同步与覆盖范围

在仓库根目录运行以下命令，再依次选择 `config` → `opencode`：

```bash
./sync-agents.sh
```

默认目标为 `~/.config/opencode/opencode.jsonc`，可通过 `OPENCODE_ROOT`
环境变量改变目标根目录。[同步脚本](../../sync-agents.sh) 直接覆盖目标文件，
不合并或自动备份已有设置。需要保留的本地配置应在同步前备份或合入源文件。

脚本使用 SHA-256 校验复制结果，不验证 OpenCode schema、插件或 MCP 是否可启动。

配置按 OpenCode V2 原生字段维护（`formatter`、`permissions`、`agents`、`plugins`、`mcp.servers`），文件使用 JSONC 语法，可写 `//` 注释说明选型与用途。V2 插件实现与 V1 不兼容，npm 插件需使用 V2 原生包。

## MCP 环境准备

- Playwright (`opencode.jsonc` 中 `mcp.servers.playwright`)：首次使用前需安装 Playwright 浏览器副本（macOS：`npx playwright install chromium`；Linux：`npx playwright install --with-deps chromium`）。Playwright 的浏览器二进制与系统 Chrome/Safari 相互独立，未安装时启动 MCP 会报 `Executable doesn't exist`。
