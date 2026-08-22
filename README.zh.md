# decky-dsh-chat

[English](README.md) | 中文

> 在游戏模式下直接跟本机 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) 对话。

一个 [Decky Loader](https://github.com/SteamDeckHomebrew/decky-loader) 插件：自动管理本机 `dsh web` 服务，并在 Deck 浏览器中打开完整的聊天界面，无需开终端。

---

## ✨ 功能

- 🟢 插件加载时自动启动本机 `dsh web` 服务（端口 3080）
- 🌐 在 Deck 浏览器中打开完整的 Harness 网页界面（走 Steam 官方外部网页接口）
- ⏹ 紧凑竖排控制面板：启动 / 停止 / 刷新
- 🔒 以 deck 用户运行，复用现有 `~/.dsh` 配置和凭据
- 🧵 与 `dsh` TUI 共享会话——聊天记录完全一致

## 📥 安装

1. 从 [Releases](../../releases) 下载 `decky-dsh-chat-v0.1.1.zip`
2. Decky Loader → ⚙️ 设置 → **Install Plugin from ZIP**（从 ZIP 安装插件）→ 选择该 zip
3. 打开 **DSH Chat** 插件（💬 图标）——服务会自动启动

> **注意：** 完整聊天界面在 Deck 自带浏览器中打开（插件面板太窄放不下）。面板本身只显示状态和控制按钮。

## 🚀 新机从零安装（全新 Steam Deck）

> 全新 Steam Deck 完整安装指南：安装的是 **`dsh` 安装版（源码构建）**，不是 `npx` 一键版——安装版离线可用、有本地 profile，且与 DSH Chat 插件完全兼容。

### 第 0 步 — 进入桌面模式

按 **STEAM** 键 → **电源** → **切换到桌面**，然后打开 **Konsole**（终端，开始菜单里找）。

### 第 1 步 —（可选）设置密码

SteamOS 默认 `deck` 用户 **sudo 免密**，本指南全程不需要密码。但建议设置一个（SSH 远程登录、需要输密码的场景会用到）：

```bash
passwd
```

可选——开启 SSH 方便远程操作：

```bash
sudo systemctl enable --now sshd
# 然后从其他设备: ssh deck@<deck-ip>
```

> 本指南**不需要** `sudo steamos-readonly disable`——所有东西都装在家目录里。只有想用 `pacman` 装系统包时才需要解除只读。

### 第 2 步 — 安装 Node.js 22+（用户级，免 sudo）

`dsh` 要求 Node `^22.19.0 || >=24.0.0`。官方文档默认你已经装好了 Node + pnpm——但全新 Steam Deck **出厂不带 Node**，所以这是唯一需要自己补的依赖。用官方二进制包装到用户目录（不动系统）：

```bash
mkdir -p ~/.local/lib/nodejs
curl -fsSL https://nodejs.org/dist/v22.23.2/node-v22.23.2-linux-x64.tar.xz \
  | tar -xJ --strip-components=1 -C ~/.local/lib/nodejs

# 链接到 ~/.local/bin
ln -sf ~/.local/lib/nodejs/bin/node     ~/.local/bin/node
ln -sf ~/.local/lib/nodejs/bin/npm      ~/.local/bin/npm
ln -sf ~/.local/lib/nodejs/bin/npx      ~/.local/bin/npx
ln -sf ~/.local/lib/nodejs/bin/corepack ~/.local/bin/corepack

# 启用 pnpm（Node 自带 corepack）
corepack enable pnpm

# 确保 ~/.local/bin 在 PATH（没有的话追加到 ~/.bashrc，然后新开终端）
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# 验证（新开一个终端）
node -v   # v22.x.x
pnpm -v   # 10.x.x
```

### 第 3 步 — 源码安装 dsh（官方原版）

和官方 "Run from source" 完全一致：

```bash
cd ~
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web        # 启动 Web UI (http://127.0.0.1:3080)
```

就这几行。**只有用 DSH Chat 插件时才需要多加一行**——插件会自己从 `PATH` 里调用 `dsh web`，所以要把 `dsh` 全局化：

```bash
ln -sf ~/deepseek-harness/apps/cli/lib/bin.js ~/.local/bin/dsh
```

任意 profile 首次启动会在 `~/.dsh/profiles/` 初始化并安装依赖（需要网络，稍等片刻）。

### 第 4 步 — 配置 API Key

**推荐——Web UI 方式（只写存储，插件启动的服务也能读到）：**

1. 启动服务：`pnpm dsh web --no-open`（如果做了上面的软链，也可以用 `dsh web --no-open`）
2. 浏览器打开 `http://127.0.0.1:3080`
3. **设置 → Providers → DeepSeek** → 粘贴来自 [platform.deepseek.com](https://platform.deepseek.com/) 的密钥 → 保存
4. 密钥存入 `~/.dsh/.credentials.yaml`（只写，不回显）

> ⚠️ 如果用这个插件，**不要**依赖 `~/.bashrc` 里的 `export DEEPSEEK_API_KEY=sk-...`：插件启动 `dsh web` 时环境是精简的，不会继承它。上面的 Web UI 方式把密钥存在所有启动方式都能读到的地方。

### 第 5 步 — 安装 Decky 和 DSH Chat

安装 Decky Loader（游戏模式或桌面模式都行，官方一键脚本）：

```bash
curl -L https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/install_release.sh | sh
```

然后安装插件：

1. 从 [Releases](../../releases) 下载 `decky-dsh-chat-v0.1.1.zip`
2. Decky Loader → ⚙️ **设置 → Install Plugin from ZIP** → 选择该 zip
3. 打开 **DSH Chat** 插件（💬 图标）

### 第 6 步 — 验收

- 打开 **DSH Chat** 插件：状态灯变绿（服务已自动启动）
- 点 **🔗 打开浏览器** → 浏览器里出现 Harness 界面 → 开聊

## ⚙️ 使用

| 按钮 | 作用 |
| --- | --- |
| 🔗 打开浏览器 | 在 Deck 浏览器中打开 Harness 网页界面 |
| ⏹ 停止服务 | 停止本机 `dsh web` 服务 |
| ⟳ 刷新状态 | 刷新服务状态 |
| ▶ 启动服务 | 启动本机 `dsh web` 服务（未运行时显示） |

## 📋 环境要求

- Decky Loader v3+（`PluginLoader` 服务）
- DeepSeek Harness 已安装于 `~/.dsh`（含 `web` profile）

## 🛠️ 开发

```bash
pnpm install          # 安装前端依赖
pnpm run build        # 构建前端到 dist/
./package.sh          # -> packages/dsh-chat-N.zip
```

## 📄 许可证

MIT
