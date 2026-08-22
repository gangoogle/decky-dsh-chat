# decky-dsh-chat

> Chat with your local [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) from Steam Deck / ROG Ally Gaming Mode.
>
> 在游戏模式下直接跟本机 DeepSeek Harness 对话。

A [Decky Loader](https://github.com/SteamDeckHomebrew/decky-loader) plugin that manages the local `dsh web` server and opens its full chat UI in the Deck's browser — no terminal needed.

一个 Decky Loader 插件：自动管理本机 `dsh web` 服务，并在 Deck 浏览器中打开完整的聊天界面，无需开终端。

---

## ✨ Features / 功能

| English | 中文 |
| --- | --- |
| 🟢 Auto-starts the local `dsh web` server (port 3080) when the plugin loads | 🟢 插件加载时自动启动本机 `dsh web` 服务（端口 3080） |
| 🌐 Opens the full Harness web UI in the Deck's browser | 🌐 在 Deck 浏览器中打开完整的 Harness 网页界面 |
| ⏹ Compact vertical panel with start / stop / refresh controls | ⏹ 紧凑竖排控制面板：启动 / 停止 / 刷新 |
| 🔒 Runs as the deck user, reuses your existing `~/.dsh` profile & credentials | 🔒 以 deck 用户运行，复用现有 `~/.dsh` 配置和凭据 |
| 🧵 Shares sessions with the `dsh` TUI — same conversation history | 🧵 与 `dsh` TUI 共享会话——聊天记录完全一致 |

## 📥 Install / 安装

**English:**

1. Download `decky-dsh-chat-v0.1.1.zip` from [Releases](../../releases)
2. Decky Loader → ⚙️ Settings → **Install Plugin from ZIP** → select the zip
3. Open the **DSH Chat** plugin (💬 icon) — the server starts automatically

**中文：**

1. 从 [Releases](../../releases) 下载 `decky-dsh-chat-v0.1.1.zip`
2. Decky Loader → ⚙️ 设置 → **Install Plugin from ZIP**（从 ZIP 安装插件）→ 选择该 zip
3. 打开 **DSH Chat** 插件（💬 图标）——服务会自动启动

> **Note / 注意:** The full chat UI opens in the Deck's built-in browser (the plugin panel is too narrow for it). The panel itself only shows status and controls.
>
> 完整聊天界面在 Deck 自带浏览器中打开（插件面板太窄放不下）。面板本身只显示状态和控制按钮。

## ⚙️ Usage / 使用

| Button / 按钮 | English | 中文 |
| --- | --- | --- |
| 🔗 打开浏览器 | Open the Harness web UI in the Deck's browser | 在 Deck 浏览器中打开 Harness 网页界面 |
| ⏹ 停止服务 | Stop the local `dsh web` server | 停止本机 `dsh web` 服务 |
| ⟳ 刷新状态 | Refresh server status | 刷新服务状态 |
| ▶ 启动服务 | Start the local `dsh web` server (shown when not running) | 启动本机 `dsh web` 服务（未运行时显示） |

## 📋 Requirements / 环境要求

- Decky Loader v3+ (`PluginLoader` service) / Decky Loader v3+（`PluginLoader` 服务）
- DeepSeek Harness installed at `~/.dsh` (with the `web` profile) / DeepSeek Harness 已安装于 `~/.dsh`（含 `web` profile）

## 🛠️ Development / 开发

```bash
pnpm install          # install frontend deps / 安装前端依赖
pnpm run build        # build frontend -> dist/ / 构建前端到 dist/
./package.sh          # -> packages/dsh-chat-N.zip
```

## 📄 License / 许可证

MIT
