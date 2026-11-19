"""Offline fixtures for the eval harness tests — the in-process driver's seams (ADR-0022 §1).

The scripted-model builders live in ``tests/support/eval_models.py``; ``install_model`` (in the
package-level conftest) injects one as the agent's base model, so ``build_agent()`` builds a real
xape agent whose only fake part is the model. The autouse ``_reset_seam`` leaves the process-global
``bash`` executor memo clean between tests — the driver (Regression Cases) builds real tools. The
benchmark's own sandbox fake is gone with ``evals/harness/sandbox.py``: a Trial now runs the sandbox
inside a ``xape run`` subprocess (``test_trial.py``). No network, no keys.
"""

from __future__ import annotations

import pytest

from xape.tools.bash import reset_executor


@pytest.fixture(autouse=True)
def _reset_seam():
    """Leave the ``xape.tools.bash`` executor seam clean after each test (the memo is process-global)."""
    yield
    reset_executor()
