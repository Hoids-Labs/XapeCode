# Getting Started with xape

Install `xape`, configure your first model provider, and start an interactive coding session.

---

## 1. Prerequisites & Installation

`xape` requires **Python 3.12+** and [uv](https://docs.astral.sh/uv/).

### macOS & Linux

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/HanishDhanwalkar/xape-ollama.git
cd xape-ollama

# Install dependencies and git hooks
make install

# Place `xape` on your PATH (tracking this checkout)
make install-cli
```

### Windows (PowerShell)

```powershell
git clone https://github.com/HanishDhanwalkar/xape-ollama.git
cd xape-ollama
.\build.ps1 install
.\build.ps1 install-cli
```

Verify your installation:
```bash
xape --version
```

---

## 2. Configure a Provider

Copy the example environment file:
```bash
cp .env.example .env
```

Select a model provider. You can run completely locally with Ollama or bring your own API key for cloud providers:

### Option A: Local & Free with Ollama ($0, Offline)
1. Install and start [Ollama](https://ollama.com).
2. Pull a tool-calling code model (e.g., `qwen2.5-coder:7b` or `qwen3:8b`):
   ```bash
   ollama pull qwen3:8b
   ```
3. Set your `.env`:
   ```ini
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=qwen3:8b
   ```

### Option B: Cloud API via Google Gemini
1. Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).
2. Set your `.env`:
   ```ini
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=your-api-key
   GEMINI_MODEL=gemini-2.5-flash
   ```

### Option C: Universal Router via OpenRouter
1. Get an API key from [OpenRouter](https://openrouter.ai).
2. Set your `.env`:
   ```ini
   LLM_PROVIDER=openrouter
   OPENROUTER_API_KEY=your-api-key
   OPENROUTER_MODEL=openrouter/free
   ```

---

## 3. Interactive REPL

Start `xape` in any project directory:
```bash
xape
```

### Keyboard Shortcuts

| Action | Shortcut | Behavior |
| :--- | :--- | :--- |
| **Send** | `Enter` | Submit prompt when idle. |
| **Steer Turn** | `Enter` (while working) | Inject mid-turn instructions into the running loop before the next tool call. |
| **Queue Follow-up** | `Alt+Enter` (while working) | Queue a follow-up turn to run immediately after the current turn ends. |
| **Abort Turn** | `Esc` | Gracefully cancel the active turn while keeping conversation history intact. |
| **Cycle Permission Mode** | `Shift+Tab` | Cycle through `default` → `edit` → `plan` → `bypass`. |
| **Toggle Verbose** | `Ctrl+O` | Show or hide internal subagent progress. |
| **Approve / Deny Tool** | `y` / `n` (or `a` for always) | Approve or deny gated tool executions (bash commands, mutations). |
| **Exit** | `Ctrl+D` or `/quit` | Save memory summaries and exit. |

---

## 4. Session Persistence & Resuming

All session logs and agent artifacts are stored under `<launch_dir>/.xape/` (gitignored):
* `.xape/sessions/*.jsonl`: Full event transcripts.
* `.xape/MEMORY.md`: Persistent cross-session project memory.
* `.xape/logs/xape.log`: Detailed runtime logs.

```bash
# Resume the most recent session in this directory
xape --resume

# Resume a specific session by its session ID
xape --resume <session-id>

# List all prior sessions with timestamps and message counts
xape sessions

# Run with ads disabled
xape --no-ads
```

---

## 5. Next Steps

* [Configuring Providers](providers.md): In-depth setup for Ollama, Gemini, OpenRouter, and Modal.
* [Sandboxing & Isolation](sandboxing.md): Running bash and file mutations in Docker or Modal containers.
* [Headless Execution](headless-and-remote.md): Running `xape run` in scripts, CI/CD, or on Modal.
* [Troubleshooting](troubleshooting.md): Diagnosing startup preflight checks and tool issues.

