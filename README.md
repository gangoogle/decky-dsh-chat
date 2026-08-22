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

## 🚀 Fresh Steam Deck Setup / 新机从零安装

> A complete guide for a brand-new Steam Deck: set up **the installed `dsh` (source build)** — not the one-shot `npx` launcher — so it works offline and with this plugin.
>
> 全新 Steam Deck 完整安装指南：安装的是 **`dsh` 安装版（源码构建）**，不是 `npx` 一键版——安装版离线可用、有本地 profile，且与 DSH Chat 插件完全兼容。

### Step 0 — Desktop Mode / 进入桌面模式

Press **STEAM** → **Power** → **Switch to Desktop**, then open **Konsole** (the terminal, from the start menu).

按 **STEAM** 键 → **电源** → **切换到桌面**，然后打开 **Konsole**（终端，开始菜单里找）。

### Step 1 — (Optional) Set a password / （可选）设置密码

SteamOS gives the `deck` user passwordless `sudo` by default — you don't need a password for this guide. Setting one is recommended for SSH and password-prompting tools:

SteamOS 默认 `deck` 用户 **sudo 免密**，本指南全程不需要密码。但建议设置一个（SSH 远程登录、需要输密码的场景会用到）：

```bash
passwd
```

Optional — enable SSH to set up the Deck remotely / 可选：开启 SSH 方便远程操作：

```bash
sudo systemctl enable --now sshd
# then from another machine / 然后从其他设备: ssh deck@<deck-ip>
```

> `sudo steamos-readonly disable` is **NOT** needed for this guide — everything installs into your home directory. It is only required if you want to install system packages with `pacman`.
>
> 本指南**不需要** `sudo steamos-readonly disable`——所有东西都装在家目录里。只有想用 `pacman` 装系统包时才需要解除只读。

### Step 2 — Install Node.js 22+ (user-level, no sudo) / 安装 Node.js 22+（用户级，免 sudo）

`dsh` requires Node `^22.19.0 || >=24.0.0`. Install the official binary tarball into your home directory:

`dsh` 要求 Node `^22.19.0 || >=24.0.0`。用官方二进制包装到用户目录（不动系统）：

```bash
mkdir -p ~/.local/lib/nodejs
curl -fsSL https://nodejs.org/dist/v22.23.2/node-v22.23.2-linux-x64.tar.xz \
  | tar -xJ --strip-components=1 -C ~/.local/lib/nodejs

# Link into ~/.local/bin / 链接到 ~/.local/bin
ln -sf ~/.local/lib/nodejs/bin/node     ~/.local/bin/node
ln -sf ~/.local/lib/nodejs/bin/npm      ~/.local/bin/npm
ln -sf ~/.local/lib/nodejs/bin/npx      ~/.local/bin/npx
ln -sf ~/.local/lib/nodejs/bin/corepack ~/.local/bin/corepack

# Enable pnpm (ships with Node via corepack) / 启用 pnpm（Node 自带 corepack）
corepack enable pnpm

# Make sure ~/.local/bin is on PATH (add once to ~/.bashrc if missing)
# 确保 ~/.local/bin 在 PATH（没有的话追加到 ~/.bashrc，然后新开终端）
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Verify / 验证（新开一个终端）
node -v   # v22.x.x
pnpm -v   # 10.x.x
```

### Step 3 — Install `dsh` from source (the installed version) / 源码安装 dsh（安装版）

> This is the **installed** build — the same thing this plugin expects on `PATH`. Unlike the one-shot `npx @deepseek-ai/dsh web`, it runs offline once built, keeps a local `~/.dsh` profile tree, and supports plugins (`dsh-tui`, `web`, …).
>
> 这是**安装版**——就是 DSH Chat 插件所依赖的 `PATH` 里的 `dsh`。和一次性 `npx @deepseek-ai/dsh web` 不同：构建一次后离线可用，维护本地 `~/.dsh` profile 体系，支持插件（`dsh-tui`、`web` 等）。

```bash
cd ~
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install          # install dependencies / 安装依赖（首次较久）
pnpm run build        # build artifacts / 构建产物

# Put dsh on PATH / 把 dsh 装进 PATH
ln -sf ~/deepseek-harness/apps/cli/lib/bin.js ~/.local/bin/dsh

# Verify / 验证
dsh --help            # usage should print / 出现用法说明即成功
```

First launch of any profile downloads/installs its bundles into `~/.dsh/profiles/` (needs network, takes a moment):

任意 profile 首次启动会在 `~/.dsh/profiles/` 初始化并安装依赖（需要网络，稍等片刻）：

```bash
dsh web --no-open     # initialize the web profile / 初始化 web profile
```

### Step 4 — Configure your API key / 配置 API Key

**Recommended — via the Web UI (write-only storage, works with this plugin):**

**推荐——Web UI 方式（只写存储，插件启动的服务也能读到）：**

1. Start the server / 启动服务：`dsh web --no-open`
2. Open `http://127.0.0.1:3080` in a browser / 浏览器打开
3. **Settings → Providers → DeepSeek** → paste your key from [platform.deepseek.com](https://platform.deepseek.com/) → Save
4. Key is stored in `~/.dsh/.credentials.yaml` (write-only) / 密钥存入 `~/.dsh/.credentials.yaml`（只写，不回显）

> ⚠️ Do **not** rely on `export DEEPSEEK_API_KEY=sk-...` in `~/.bashrc` if you use this plugin: the plugin spawns `dsh web` with a minimal environment and won't inherit it. The Web UI method above stores the key where every launch can read it.
>
> ⚠️ 如果用这个插件，**不要**依赖 `~/.bashrc` 里的 `export DEEPSEEK_API_KEY=sk-...`：插件启动 `dsh web` 时环境是精简的，不会继承它。上面的 Web UI 方式把密钥存在所有启动方式都能读到的地方。

### Step 5 — Install Decky Loader + DSH Chat / 安装 Decky 和 DSH Chat

Install Decky Loader (back in Gaming Mode, or from Desktop — the installer works either way):

安装 Decky Loader（游戏模式或桌面模式都行，官方一键脚本）：

```bash
curl -L https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/install_release.sh | sh
```

Then install the plugin / 然后安装插件：

1. Download `decky-dsh-chat-v0.1.1.zip` from [Releases](../../releases)
2. Decky Loader → ⚙️ **Settings → Install Plugin from ZIP** → select the zip
3. Open **DSH Chat** (💬 icon) / 打开 **DSH Chat** 插件（💬 图标）

### Step 6 — Verify / 验收

- Open the **DSH Chat** plugin: the status dot should turn green (server auto-started) / 打开插件，状态灯变绿（服务已自动启动）
- Tap **🔗 打开浏览器** → the Harness UI opens in the Deck's browser → start chatting / 点「打开浏览器」→ 浏览器里出现 Harness 界面 → 开聊

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
