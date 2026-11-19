# Sandboxing & Execution Isolation

`xape` routes all shell commands (`bash`) and file operations through a unified `SandboxExecutor` seam. This isolates side effects and protects host environments from accidental or untrusted code execution.

---

## 1. Sandbox Modes

Configure the active mode in `.env` via `SANDBOX_MODE`:

| Mode | Runtime Environment | Workspace Location | Best For |
| :--- | :--- | :--- | :--- |
| **`none`** (Default) | Host machine | Launch current working directory | Trusted projects, direct local editing. |
| **`docker`** | Local Docker container | Host `.xape/sandbox` bind-mounted to `/workspace` | Containing accidental breakage locally. |
| **`modal`** | Remote Modal cloud container | Ephemeral remote sandbox | Running untrusted third-party code safely. |

---

## 2. Local Docker Sandboxing

### Prerequisites
* Docker Desktop or Docker Engine installed and running.
* Current user permitted to execute `docker` without password prompts.

### Configuration
```ini
SANDBOX_MODE=docker
SANDBOX_IMAGE=ghcr.io/astral-sh/uv:python3.12-bookworm-slim
SANDBOX_WORKSPACE_DIR=.xape/sandbox
```

### How It Works
* Each tool command executes in a fresh container process (`fresh-exec`). The filesystem in `/workspace` persists across calls, while environment variable mutations and `cd` calls do not leak between turns.
* Harness artifacts (`.xape/sessions/`, `.xape/MEMORY.md`, logs) anchor to your host launch directory (`Harness Home`), keeping session history outside the sandbox.

---

## 3. Remote Modal Sandboxing

Run code execution in isolated, remote cloud containers powered by [Modal](https://modal.com).

### Configuration
```ini
SANDBOX_MODE=modal
SANDBOX_TIMEOUT_S=600.0
```

### Execution Lifecycle
1. **Startup:** `xape` prepares an empty workspace or clones the specified repository.
2. **Sync:** The workspace is uploaded to the remote Modal sandbox container.
3. **Execution:** File reading, editing, and bash commands run remotely inside the sandbox.
4. **Shutdown / Export:** When the session concludes, the modified workspace is swept back host-side into `.xape/sandbox`.

---

## 4. Git Hand-Back & Session Branches

When working inside a sandboxed workspace against a repository:

1. **Automatic Branch Creation:** All changes made by the model are secured onto a deterministic git branch:
   `xape/<session-id>`
2. **Host-Side Ambient Credentials:** The final branch push runs host-side against `.xape/sandbox` using your machine's ambient git credentials. **No GitHub tokens or credentials need to enter the sandbox.**
3. **Manual Hand-Back:** At any point while idle in the REPL, type:
   ```text
   /ship
   ```
   `xape` will sync the sandbox state, auto-commit uncommitted model changes, and push the branch to your remote.

---

## 5. Sandboxed Git Pushes (`SANDBOX_GIT_TOKEN`)

If your workflow requires the sandboxed agent itself to push branches or create Pull Requests directly from within the container (e.g., using the `gh` CLI):

1. Set `SANDBOX_GIT_TOKEN` in `.env`:
   ```ini
   SANDBOX_GIT_TOKEN=ghp_yourScopedRevocablePAT
   ```
2. Both Docker and Modal backends inject this token as `GITHUB_TOKEN` directly into the worker environment, configuring git's credential helper (`x-access-token:$GITHUB_TOKEN`).
3. **Security Invariant:** Only hand the sandbox a scoped, revocable Personal Access Token (PAT). When unset, the sandbox holds zero credentials, and host-side Hand-Back still ships your branch securely.

