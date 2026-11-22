"""The Headless Runtime — a plain ``asyncio.run`` around ``build_agent()`` for ``xape run`` (ADR-0019 §1).

One entrypoint, :func:`~xape.runtime.headless.run_headless_task`: bypass permissions, ``ask_user``
as a no-op, the sandbox Workspace + host-side Hand-back, and Langfuse tracing. Beside it sits the
Recording Seam (:mod:`xape.runtime.recording`) — the one function that decides whether a built
agent runs wrapped in ``kitaru_pydantic_ai.KitaruAgent``, and xape's only kitaru import site
(ADR-0019 §3, ADR-0021 §5). The REPL records too, so :mod:`xape.tui.app` imports the seam and —
package ``__init__`` being what it is — this module with it; what the REPL still never pulls in is
kitaru, because the seam's kitaru imports live inside its configured branch (proved in a fresh
interpreter by ``tests/unit/xape/test_cli.py``).
"""

from __future__ import annotations

from xape.runtime.headless import RUN_SPAN_NAME, run_headless_task

__all__ = [
    "RUN_SPAN_NAME",
    "run_headless_task",
]
