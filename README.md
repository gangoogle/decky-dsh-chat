# decky-dsh-chat

English | [中文](README.zh.md)

> Chat with your local [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) from Steam Deck / ROG Ally Gaming Mode.

A [Decky Loader](https://github.com/SteamDeckHomebrew/decky-loader) plugin that manages the local `dsh web` server and opens its full chat UI in the Deck's browser — no terminal needed.

---

## ✨ Features

- 🟢 Auto-starts the local `dsh web` server (port 3080) when the plugin loads
- 🌐 Opens the full Harness web UI in the Deck's browser via the Steam external-web navigator
- ⏹ Compact vertical panel with start / stop / refresh controls
- 🔒 Runs as the deck user, reuses your existing `~/.dsh` profile and credentials
- 🧵 Shares sessions with the `dsh` TUI — same conversation history

## 📥 Install

1. Download `decky-dsh-chat-v0.1.1.zip` from [Releases](../../releases)
2. Decky Loader → ⚙️ Settings → **Install Plugin from ZIP** → select the zip
3. Open the **DSH Chat** plugin (💬 icon) — the server starts automatically

> **Note:** The full chat UI opens in the Deck's built-in browser (the plugin panel is too narrow for it). The panel itself only shows status and controls.

## 🚀 Fresh Steam Deck Setup

> A complete guide for a brand-new Steam Deck: set up **the installed `dsh` (source build)** — not the one-shot `npx` launcher — so it runs offline and works with this plugin.

### Step 0 — Desktop Mode

Press **STEAM** → **Power** → **Switch to Desktop**, then open **Konsole** (the terminal, from the start menu).

### Step 1 — (Optional) Set a password

SteamOS gives the `deck` user passwordless `sudo` by default — you don't need a password for this guide. Setting one is recommended for SSH and password-prompting tools:

```bash
passwd
```

Optional — enable SSH to set up the Deck remotely:

```bash
sudo systemctl enable --now sshd
# then from another machine: ssh deck@<deck-ip>
```

> `sudo steamos-readonly disable` is **NOT** needed for this guide — everything installs into your home directory. It is only required if you want to install system packages with `pacman`.

### Step 2 — Install Node.js 22+ (user-level, no sudo)

`dsh` requires Node `^22.19.0 || >=24.0.0`. Install the official binary tarball into your home directory:

```bash
mkdir -p ~/.local/lib/nodejs
curl -fsSL https://nodejs.org/dist/v22.23.2/node-v22.23.2-linux-x64.tar.xz \
  | tar -xJ --strip-components=1 -C ~/.local/lib/nodejs

# Link into ~/.local/bin
ln -sf ~/.local/lib/nodejs/bin/node     ~/.local/bin/node
ln -sf ~/.local/lib/nodejs/bin/npm      ~/.local/bin/npm
ln -sf ~/.local/lib/nodejs/bin/npx      ~/.local/bin/npx
ln -sf ~/.local/lib/nodejs/bin/corepack ~/.local/bin/corepack

# Enable pnpm (ships with Node via corepack)
corepack enable pnpm

# Make sure ~/.local/bin is on PATH (add once to ~/.bashrc if missing)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Verify (in a new terminal)
node -v   # v22.x.x
pnpm -v   # 10.x.x
```

### Step 3 — Install `dsh` from source (the installed version)

> This is the **installed** build — the same thing this plugin expects on `PATH`. Unlike the one-shot `npx @deepseek-ai/dsh web`, it runs offline once built, keeps a local `~/.dsh` profile tree, and supports plugins (`dsh-tui`, `web`, …).

```bash
cd ~
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install          # install dependencies (first run takes a while)
pnpm run build        # build artifacts

# Put dsh on PATH
ln -sf ~/deepseek-harness/apps/cli/lib/bin.js ~/.local/bin/dsh

# Verify
dsh --help            # usage should print
```

First launch of any profile downloads/installs its bundles into `~/.dsh/profiles/` (needs network, takes a moment):

```bash
dsh web --no-open     # initialize the web profile
```

### Step 4 — Configure your API key

**Recommended — via the Web UI (write-only storage, works with this plugin):**

1. Start the server: `dsh web --no-open`
2. Open `http://127.0.0.1:3080` in a browser
3. **Settings → Providers → DeepSeek** → paste your key from [platform.deepseek.com](https://platform.deepseek.com/) → Save
4. The key is stored in `~/.dsh/.credentials.yaml` (write-only)

> ⚠️ Do **not** rely on `export DEEPSEEK_API_KEY=sk-...` in `~/.bashrc` if you use this plugin: the plugin spawns `dsh web` with a minimal environment and won't inherit it. The Web UI method above stores the key where every launch can read it.

### Step 5 — Install Decky Loader + DSH Chat

Install Decky Loader (from Gaming Mode or Desktop — the official one-liner):

```bash
curl -L https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/install_release.sh | sh
```

Then install the plugin:

1. Download `decky-dsh-chat-v0.1.1.zip` from [Releases](../../releases)
2. Decky Loader → ⚙️ **Settings → Install Plugin from ZIP** → select the zip
3. Open **DSH Chat** (💬 icon)

### Step 6 — Verify

- Open the **DSH Chat** plugin: the status dot should turn green (server auto-started)
- Tap **🔗 打开浏览器** → the Harness UI opens in the Deck's browser → start chatting

## ⚙️ Usage

| Button | Action |
| --- | --- |
| 🔗 打开浏览器 | Open the Harness web UI in the Deck's browser |
| ⏹ 停止服务 | Stop the local `dsh web` server |
| ⟳ 刷新状态 | Refresh server status |
| ▶ 启动服务 | Start the local `dsh web` server (shown when not running) |

## 📋 Requirements

- Decky Loader v3+ (`PluginLoader` service)
- DeepSeek Harness installed at `~/.dsh` (with the `web` profile)

## 🛠️ Development

```bash
pnpm install          # install frontend dependencies
pnpm run build        # build frontend -> dist/
./package.sh          # -> packages/dsh-chat-N.zip
```

## 📄 License

MIT
