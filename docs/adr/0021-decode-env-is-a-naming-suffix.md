# 0021. `XAPE_ENV` is a naming suffix; one secret store per platform

Status: Accepted
Date: 2026-09-09

Supersedes [ADR-0015](0015-environment-bucket-secrets.md) §§1–3, 5, 7 (the Environment Bucket and the
`XAPE_ENV`-gated source chain) and [ADR-0020](0020-remote-headless-on-modal.md) §11 (the Modal Secret picks
`XAPE_ENV`). ADR-0015 §4 (the deleted `RUNTIME_SECRET_*` knobs) and
§9 (the `.env.example` drift test) stand unchanged; §6 was already moot.

## Context

ADR-0015 gave `XAPE_ENV` one job: **select where `Settings` reads from**. `local` read `.env`; `dev` /
`staging` / `prod` read the **Environment Bucket** — a Kitaru secret named `xape-<env>` — and dropped `.env`
from the chain entirely, so a missing key failed loudly.

Two things turned out to be true about that design.

**It made Kitaru a hard startup dependency of everything.** Kitaru's role in this project is recording and
replay: an evals layer, opt-in, observed by a human ([ADR-0019](0019-kitaru-replay-runtime.md) §3). But
`XAPE_ENV=prod` also made it the *config store*, so every remote-environment run — REPL, `xape run`, and
every Modal container — had to reach a Kitaru workspace, authenticated, before its first prompt. ADR-0019 §3's
invariant already had to carve out a third branch for it ("or a remote-bucket context"). That coupling is what
we actually hit in practice: a deployed `xape-headless` whose Secret said `XAPE_ENV=prod` refused every run
with `the environment bucket 'xape-prod' could not be loaded` — no bucket had been created, and the
`ZENPROKEY_…` a container needs to read one is still unminted (`tasks/153`). The runs failed at startup,
`session=None`, for a reason that had nothing to do with the task, the provider, or the sandbox.

**Nothing else ever read the bucket.** `Settings` was its only reader. The Kitaru Worker attaches no secret to
a run spec, and `scripts/register_kitaru_agent.py` went as far as pinning `XAPE_ENV=local` into every replay
spec *specifically to keep a spawn from inheriting a bucket*. A store with one reader, which another part of
the same system works to avoid, is not a store — it is a coupling.

Meanwhile the question `XAPE_ENV` is genuinely good at answering was already being answered elsewhere and
well: `xape-sandbox-<env>` (the nested Modal sandbox app) derives from it so a `local` experiment
cannot disturb a `prod` one. Langfuse projects are selected separately by their API keys.

There is a second, quieter problem. ADR-0020 §11 put `XAPE_ENV` **inside** the Modal Secret. A Secret is
mutable by an operator and re-read at container start, so the deployment's identity ("which environment am I?")
lived in a place the deployment did not control — and `modal secret create --force` writes a *new* Secret
object, which a running deployment does not pick up until it is redeployed. The observed symptom: a Secret
rewritten to `XAPE_ENV=local` while every container kept reading `prod`.

## Decision

**`XAPE_ENV` names the environment. It never decides where config is read from.**

1. **One source chain, at every environment.** `init > process env > .env > defaults` — pydantic-settings'
   default chain, with no `settings_customise_sources` override at all. `EnvironmentBucketSettingsSource`,
   `_read_bucket`, `bucket_load_error`, `environment_bucket_name` and the out-of-band `_resolve_xape_env`
   bootstrap are **deleted**; `xape_env` becomes an ordinary field read like every other. The store that
   feeds the chain is the platform's own: a developer's `.env` on a laptop, the Modal Secret in a container.

2. **One environment, one deployment, one Secret.** Both Modal apps take the `-<env>` suffix their sandbox app
   already had: `xape-headless-<env>` and `xape-kitaru-worker-<env>`, each running with
   the Secret of the same name. `XAPE_ENV=prod xape remote deploy` publishes `xape-headless-prod`; a
   plain deploy publishes `xape-headless-local`. `xape remote run|attempts|logs` resolve the same name
   from `settings.xape_env`, so the launcher and the deployment cannot mean different apps. A Secret carries
   **credentials**, and is the whole config surface for its container.

3. **The environment is baked, not carried.** `build_image(xape_env=…)` sets `XAPE_ENV` in the image at
   deploy, from the deploying laptop's env — the same value that just named the app and its Secret, so the
   three cannot drift. A Secret that carries its own `XAPE_ENV` and disagrees is refused at startup with ONE
   friendly line (`xape_env_mismatch_error`), because Modal's env precedence would otherwise make an app
   called `xape-headless-local` file `xape-prod` traces silently. An unknown value fails on the laptop at
   deploy (`deploy_time_xape_env`), not in a container log. `xape remote deploy` passes `XAPE_ENV`
   **explicitly** to the `modal deploy` subprocess: it re-imports the app module and reads `os.environ`, and a
   value that came from `.env` reached `Settings` without ever landing there.

4. **A replay runs AS the environment of the Worker that spawned it.** `register_kitaru_agent.py` no longer
   pins `XAPE_ENV` into the run spec. There is no bucket left to inherit, and a replay spawned by
   `xape-kitaru-worker-prod` should file its traces under `xape-prod` — not under whatever a registration
   script guessed months earlier. A run spec change means a new Agent Version.

5. **Clean break: the Environment Bucket is deleted**, and `scripts/sync_secrets.py` + `make sync-secrets` +
   `tests/support/kitaru_secrets.py` with it — the script existed only to write the store, and the store has
   no readers left. No shim, no compat path, in keeping with ADR-0015 §4's own precedent. **Kitaru is an
   evals/recording layer and nothing else**, which *tightens* ADR-0019 §3's invariant rather than loosening it:
   its third branch is gone, so recording (or a Worker Task) is now the ONLY thing that can import kitaru, at
   any `XAPE_ENV`.

**Non-goals.** `XAPE_ENV` still does not change session dirs, log paths or `MEMORY.md`. The `Literal` stays
closed — a new environment is a code change, deliberately. No secret store is introduced to replace the
bucket: if a deployment needs a key, it goes in that deployment's Secret.

## Diagram

```mermaid
flowchart TB
    subgraph BEFORE["ADR-0015 — XAPE_ENV selected the SOURCE"]
        direction TB
        B_ENV{{"XAPE_ENV"}}
        B_DOT[".env"]
        B_BUCKET["Environment Bucket<br/>Kitaru secret xape-&lt;env&gt;<br/>(kitaru imported at startup)"]
        B_SET[("Settings")]
        B_ENV -->|local| B_DOT --> B_SET
        B_ENV -->|dev/staging/prod<br/>.env DROPPED| B_BUCKET --> B_SET
    end

    subgraph AFTER["ADR-0021 — XAPE_ENV names things"]
        direction TB
        A_PROC["process env<br/>(the Modal Secret, in a container)"]
        A_DOT[".env<br/>(a laptop)"]
        A_DEF["defaults"]
        A_SET[("Settings<br/>ONE chain, every environment")]
        A_PROC --> A_SET
        A_DOT --> A_SET
        A_DEF --> A_SET
        A_SET --> A_NAMES["names, and only names:<br/>xape-headless-&lt;env&gt;<br/>xape-kitaru-worker-&lt;env&gt;<br/>xape-sandbox-&lt;env&gt;"]
        A_KIT["kitaru<br/>recording · replay · evals"]
        A_SET -. "imported ONLY when recording<br/>is configured, or under a Worker Task" .-> A_KIT
    end

    BEFORE ==>|superseded| AFTER

    classDef gone fill:#ffd6d6,stroke:#c62828,color:#7f1d1d;
    classDef truth fill:#fff3cd,stroke:#b8860b,color:#7a5c00,stroke-width:3px;
    classDef good fill:#d4edda,stroke:#2e7d32,color:#1b5e20;
    class B_BUCKET,BEFORE gone;
    class A_SET,B_SET truth;
    class A_NAMES,A_KIT,AFTER good;
```

## Consequences

**Positive.** A deployed run no longer depends on a Kitaru workspace being reachable, provisioned and
authenticated — the failure that motivated this ADR is unrepresentable, and `tasks/153`'s unminted key now
gates only the Kitaru Worker, which is the only thing that actually needs a workspace. `Settings` loses ~130
lines, one settings source, a thread-pool event-loop workaround and a module-global error channel; the whole
of `settings_customise_sources` goes with them. Two environments are two apps with two Secrets, so
"redeploy `prod`" and "point at `prod`" are the same sentence. ADR-0019 §3's invariant gets simpler: no
`XAPE_ENV` imports kitaru.

**Negative / accepted.**

- **`.env` can backfill a key at any environment.** ADR-0015 §2's loud-failure property is gone: at
  `XAPE_ENV=prod` on a laptop, a key missing from wherever you meant it to come from is silently filled from
  `.env`. Accepted — a container has no `.env` at all, so the property still holds where it was doing real
  work, and "the deployment's Secret is its config" is a rule an operator can hold in their head.
- **Credentials must be mirrored by hand into each environment's Secret.** There is no `make sync-secrets`
  any more. For two Modal apps and a handful of keys this is one documented `modal secret create` per app;
  a project with many environments would want tooling, and would then be choosing it deliberately.
- **A laptop `XAPE_ENV=prod` reads your `.env` and files traces under `xape-prod`.** That is the intended
  reading of "naming only", but it is a change in meaning for anyone who read `prod` as "and get prod's
  secrets".
- **Existing deployments must be recreated**, not migrated: `xape-headless` (unsuffixed) is a different app
  from `xape-headless-local`, and its Secret is a different Secret. Stop the old app, create the suffixed
  Secret, redeploy.
- **The Kitaru Worker's Agent Version must be re-registered** (§4 changed the run spec) — versions are
  immutable, so this is a new version, and replays must be pinned to it.
