# Headless Execution & Remote Deployments

`xape` can run without an interactive TUI for automated scripts, CI/CD pipelines, and serverless remote jobs.

---

## 1. Local Headless Execution (`xape run`)

Run a single autonomous turn from your shell:

```bash
# Basic headless run
xape run "Fix the type errors reported by mypy in src/xape/sponsors/"

# Run against a specific git repository inside a sandbox
xape run --repo https://github.com/your-org/your-repo.git "Add unit tests for user auth"

# Override the active model for this execution
xape run --model qwen3:8b "Refactor the database queries in app.py"

# Enforce a maximum model-request budget
xape run --max-requests 50 "Audit security issues in dependencies"
```

### Headless Permission Defaults
In headless mode where no human terminal is available to answer permission prompts, mutating tool calls adhere to strict safety: any ungated mutating command that requires human approval fails safely and records the refusal reason in the execution transcript.

---

## 2. Remote Headless App on Modal (`xape remote`)

Deploy `xape` as a serverless remote application on [Modal](https://modal.com) to execute long-running tasks, nightly jobs, or webhook-triggered agent runs in the cloud.

### Prerequisites
* Modal authenticated CLI (`uv run modal token set`).
* Deployment environment named via `XAPE_ENV` (defaults to `local`, or `dev`/`prod`).

### Commands

#### Deploy the Headless App
```bash
# Deploys the headless app image and secrets
xape remote deploy
```

#### Trigger a Remote Run
```bash
xape remote run "Audit outdated dependencies and open a draft PR"
```

#### Monitor Remote Jobs
```bash
# List recent remote execution attempts
xape remote attempts

# Stream live container logs
xape remote logs
```

---

## 3. Remote Triggers (Webhooks & Crons)

When deployed on Modal, the remote headless harness exposes:
1. **Authenticated Webhook:** Fire autonomous jobs via HTTP POST requests authenticated with your proxy tokens.
2. **Scheduled Crons:** Configure recurring executions (e.g. nightly test runs, dependency updates) defined in `src/xape/remote/app.py`.

