# Troubleshooting

Common issues, startup preflight messages, and their solutions.

---

## 1. Startup Preflights & Keys

| Symptom / Log Message | Cause | Resolution |
| :--- | :--- | :--- |
| `Decode: set GEMINI_API_KEY in your environment or .env` | `LLM_PROVIDER=gemini` but API key is missing or set to placeholder. | Add your real API key to `.env` or run `export GEMINI_API_KEY=...`. |
| `Decode: LLM_PROVIDER=openrouter needs OPENROUTER_API_KEY` | `LLM_PROVIDER=openrouter` but key is unset. | Add `OPENROUTER_API_KEY=sk-or-...` to `.env`. |
| `Decode: could not reach Ollama at ...` | Ollama service is stopped or port is blocked. | Start Ollama (`ollama serve`) and verify `OLLAMA_BASE_URL=http://localhost:11434`. |
| `Decode: no Ollama models found` | Ollama is reachable but no models have been pulled. | Run `ollama pull qwen3:8b` (or your chosen model). |
| `Decode: set OLLAMA_MODEL for headless runs` | `xape run` launched with Ollama without specifying a target model. | Set `OLLAMA_MODEL=qwen3:8b` in `.env` or pass `--model qwen3:8b`. |
| `Decode: LLM_PROVIDER=modal needs MODAL_ENDPOINT_URL` | Modal provider selected without an endpoint. | Deploy an endpoint via `modal endpoint create` and paste the URL into `.env`. |
| `HTTP 429 Too Many Requests` | Hit provider rate limits (e.g. Gemini free tier). | Switch models via `/model` or use local Ollama models. |

---

## 2. Sandboxing & Docker

| Symptom / Log Message | Cause | Resolution |
| :--- | :--- | :--- |
| `docker: command not found` | Docker CLI is not installed or not in system PATH. | Install Docker Desktop or Docker Engine. |
| `Docker daemon unreachable` | Docker engine service is not running. | Start Docker Desktop / dockerd service. |
| `Permission denied while connecting to docker.sock` | Non-root user lacks docker group permissions on Linux. | Run `sudo usermod -aG docker $USER` and reload shell. |

---

## 3. LSP & Code Intelligence

| Symptom / Log Message | Cause | Resolution |
| :--- | :--- | :--- |
| `LSP diagnostics return empty / no errors detected` | `ty` language server executable is missing. | Run `make install` to install dev dependencies including `ty`. |
| Slow LSP diagnostics | Large codebase indexing delay. | Diagnostics are best-effort and run passively after edits without blocking. |

---

## 4. Debug Logs

To enable detailed logging:
1. Set `LOG_LEVEL=DEBUG` in `.env`.
2. Inspect log outputs at `.xape/logs/xape.log`.

