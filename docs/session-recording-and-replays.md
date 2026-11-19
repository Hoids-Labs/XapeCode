# Session Recording & Deterministic Replays

`xape` integrates with [Kitaru](https://www.zenml.io/product/kitaru) to record interactive and headless developer sessions and run deterministic what-if replays from the terminal.

---

## 1. Local Recording Setup

Start a local Kitaru server:
```bash
make kitaru-local
```
This runs an open-source Kitaru instance at `http://localhost:8000` and outputs a registered `KITARU_AGENT_ID`.

Add them to `.env`:
```ini
KITARU_API_URL=http://localhost:8000
KITARU_AGENT_ID=your-agent-id
```

When configured, every interactive turn or `xape run` files a full Kitaru Session capturing model inputs, tool arguments, and environment state.

---

## 2. Inspecting Sessions

```bash
# Check Kitaru connection status
uv run kitaru status

# View recorded sessions
uv run kitaru session list

# Inspect an individual session by ID
uv run kitaru session get <session-id>
```

---

## 3. Running Replays

A replay re-executes a recorded session from the top to evaluate changes in models, prompts, or tool policies:

### Baseline Replay
Runs an exact control replay:
```bash
uv run kitaru replay create <session-id> --agent xape@latest
```

### What-If Replay (Model Override)
Re-run a failure session using a different model to evaluate whether a different model fixes the bug:
```bash
uv run kitaru replay create <session-id> --agent xape@latest --override '{"model": "qwen3:8b"}'
```

### Local Workers
Replays run locally on your machine via a Kitaru Worker:
```bash
uv run kitaru worker start
```

