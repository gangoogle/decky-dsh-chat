# decky-dsh-chat

Chat with your local [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) from Steam Deck / ROG Ally Gaming Mode.

在游戏模式里直接跟本机 DeepSeek Harness 对话。

## Features

- 🟢 Auto-starts the local `dsh web` server (port 3080) when the plugin loads
- 🌐 Opens the full Harness web UI in the Deck's browser via the Steam external-web navigator
- ⏹ Start / stop / refresh controls in a compact vertical panel
- 🔒 Runs as the deck user, reuses your existing `~/.dsh` profile and credentials
- 🧵 Sessions are shared with the `dsh` TUI — same conversation history

## Install

1. Download `dsh-chat-*.zip` from [Releases](../../releases)
2. Decky Loader → ⚙️ Settings → **Install Plugin from ZIP** → pick the zip
3. Open the **DSH Chat** plugin (💬 icon)

> The web UI needs a browser, so it opens in the Deck's built-in browser — the plugin panel itself only shows status and controls.

## Requirements

- Decky Loader v3+ (`PluginLoader` service)
- DeepSeek Harness installed at `~/.dsh` (profiles: `dsh` / `dsh-tui` / `dsh web`)

## Development

```bash
pnpm install
pnpm run build   # frontend -> dist/
./package.sh     # -> packages/dsh-chat-N.zip
```

## License

MIT
