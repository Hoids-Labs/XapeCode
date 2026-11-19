---
id: 154-xape-remote-cli
feature: remote-headless
status: done
---

# `xape remote` — the Modal launcher under the xape CLI

## Scope
Move the Modal Headless App launcher from `scripts/modal_headless.py` (`modal run …::main` /
`::attempts`) under the `xape` CLI as `xape remote deploy|run|attempts|logs`, with the app
itself in `xape/remote/`. Drop the ephemeral-app path: every trigger targets the deployment.

## Acceptance criteria
- [x] `xape remote run "<task>" [--repo --sandbox-mode --model --timeout-seconds --max-requests]` runs one task on the deployed app, streams the answer, exits with the run's code.
- [x] `xape remote attempts "<task>" --repo <url> --attempts N [--detach]` = the former `::attempts`, same table / notes / diff tail / exit semantics.
- [x] `xape remote deploy` = `modal deploy -m xape.remote.app`, refused with one line outside a checkout; `XAPE_NIGHTLY_*` still read at deploy.
- [x] `xape remote logs` = `modal app logs xape-headless`.
- [x] Client-side guards unchanged (docker mode, fan-out without repo, zero attempts): one friendly line, no container. Missing deployment / missing Modal creds: one friendly line.
- [x] `import xape.cli` imports no `modal` (unit test pins it).
- [x] Worker script + agent registration import the image builder from `xape.remote.image`; both apps still share the layout constants.
- [x] Docs: 07_infra.md rewritten for the new verbs; ADR-0020 Amendment §10; glossary + AGENTS.md updated.
- [ ] [HUMAN] `uv run xape remote deploy` then `uv run xape remote run "print uname -a" --sandbox-mode none` reports a gVisor kernel.

## Out of scope
- Moving the Kitaru Worker under `xape remote worker` (no second caller).
- An `--ephemeral` flag re-creating `modal run`'s no-deploy path.

## Log
### [SWE] 2026-09-03 — Implemented
`src/xape/remote/{__init__,headless,image,app,cli}.py`; `scripts/modal_headless.py` +
`scripts/modal_image.py` removed; tests moved to `tests/unit/xape/remote/`; 351 affected unit
tests green. Human deploy gate left open.
