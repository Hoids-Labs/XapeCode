"""Shared pytest fixtures for eval tests (evals/harness and evals/regression suites)."""

from __future__ import annotations

from pathlib import Path

import pytest
from support.benchmark_tasks import write_task_dir

from xape.services.lsp import service as lsp_service


@pytest.fixture(autouse=True)
def _clear_lsp_cache():
    """Isolate the module-level per-root cache between tests (it persists across calls by design)."""
    lsp_service._CLIENTS.clear()
    yield
    lsp_service._CLIENTS.clear()


@pytest.fixture
def greeting_task_dir(tmp_path: Path) -> Path:
    """A synthetic v2 benchmark task directory (001-greeting).

    Uses the builder from ``support.benchmark_tasks`` to create a contract-clean task folder
    suitable for use by the eval driver and benchmark system. The task has:
    - A valid task.toml with metadata
    - An instruction.md with the greeting prompt
    - A test.sh verifier that checks for a greeting response
    - A solve.sh solution script
    """
    task_name = "001-greeting"
    task_dir = tmp_path / task_name
    task_dir.mkdir(parents=True, exist_ok=True)
    return write_task_dir(task_dir)
