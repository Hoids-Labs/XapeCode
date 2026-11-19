# Model Providers & Inference Configuration

`xape` features a pluggable LLM Gateway supporting local on-device models and frontier cloud APIs. You can switch between configured providers at any time during an interactive session using `/model`.

---

## 1. Supported Providers Overview

| Provider | Key Required | Cost | Best For |
| :--- | :--- | :--- | :--- |
| **Ollama** | No | $0 (Local) | Offline development, 100% data privacy, zero API costs. |
| **Gemini** | Yes (`GEMINI_API_KEY`) | Free tier / Pay-per-token | High speed, large 1M context windows, general coding. |
| **OpenRouter** | Yes (`OPENROUTER_API_KEY`) | Free router / Pay-per-token | Multi-vendor model access, fallback routing. |
| **Modal** | Yes (Proxy token pair) | Pay-per-GPU-second | Self-hosted open weights (e.g. Qwen 35B) with dedicated compute. |

---

## 2. Ollama (Local Compute)

Run models entirely on your local machine using [Ollama](https://ollama.com).

### Setup
1. Download and install Ollama from [ollama.com](https://ollama.com).
2. Pull a tool-calling code model. Recommended models:
   ```bash
   ollama pull qwen3:8b
   # or
   ollama pull qwen2.5-coder:7b
   ```
3. Configure `.env`:
   ```ini
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=qwen3:8b
   ```

*Note: For interactive sessions, `xape` auto-discovers all locally pulled models from `GET /api/tags`. For headless runs (`xape run`), ensure `OLLAMA_MODEL` is set in `.env` or passed via `--model <name>`.*

---

## 3. Google Gemini

Fast proprietary intelligence via Google AI Studio.

### Setup
1. Create an API key at [Google AI Studio](https://aistudio.google.com).
2. Configure `.env`:
   ```ini
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=your-api-key
   GEMINI_MODEL=gemini-2.5-flash
   ```

`xape` automatically queries the Gemini API for supported tool-calling models when you use `/model`.

---

## 4. OpenRouter

Access hundreds of open-source and commercial models through a unified OpenAI-compatible endpoint.

### Setup
1. Create an account and key at [OpenRouter](https://openrouter.ai).
2. Configure `.env`:
   ```ini
   LLM_PROVIDER=openrouter
   OPENROUTER_API_KEY=your-api-key
   # Uses the free models router by default:
   OPENROUTER_MODEL=openrouter/free
   ```

---

## 5. Modal (Self-Hosted GPU Endpoints)

Serve open-weights models (e.g., `Qwen/Qwen3.6-35B-A3B-FP8`) on dedicated serverless cloud GPUs using [Modal](https://modal.com).

### Setup
1. Create a free account on [Modal](https://modal.com).
2. Generate an API token in Modal Dashboard -> Settings -> API Tokens.
3. Authenticate the project CLI:
   ```bash
   uv run modal token set --token-id <token-id> --token-secret <token-secret>
   ```
4. Deploy a model endpoint:
   ```bash
   uv run modal endpoint create --model Qwen/Qwen3.6-35B-A3B-FP8 --env main
   ```
5. Mint a proxy token pair to secure incoming requests:
   ```bash
   uv run modal workspace proxy-tokens create
   ```
   Save the generated `Modal-Key` and `Modal-Secret`.
6. Configure `.env`:
   ```ini
   LLM_PROVIDER=modal
   MODAL_ENDPOINT_URL=https://your-workspace--your-endpoint.modal.run
   MODAL_ENDPOINT_MODEL=Qwen/Qwen3.6-35B-A3B-FP8
   MODAL_PROXY_TOKEN_ID=wk-...
   MODAL_PROXY_TOKEN_SECRET=ws-...
   ```

---

## 6. Dynamic Switching with `/model`

During an active session, type:
```text
/model
```
`xape` will query all providers that have credentials or local endpoints configured and display a radiolist dialog. When you select a new model:
* The active LLM is reconstructed using that provider's credentials.
* The context window and compaction thresholds adapt immediately.
* Exploration subagents and memory summarizers automatically adopt the new provider for future turns.

