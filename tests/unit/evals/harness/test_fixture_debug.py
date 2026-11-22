"""Simple debug test for fixture."""

from pathlib import Path

import pytest
from support.eval_models import read_then_finish

from evals.harness.driver import run_agent_once

_NOTES = "notes.txt"
_NOTES_BODY = "remember to ship the eval suite"
_FINAL = "I read the notes file"


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    """A temp working tree with a readable notes file."""
    (tmp_path / _NOTES).write_text(_NOTES_BODY, encoding="utf-8")
    return tmp_path


@pytest.mark.asyncio
async def test_fixture_is_called_1(workspace, install_model):
    """Debug test 1."""
    print("\nTest 1: Calling install_model...")
    install_model(read_then_finish(_NOTES, _FINAL))
    print("Test 1: install_model called")

    record = await run_agent_once("read the notes file", cwd=workspace)
    print(f"Test 1: record.output = {record.output[:50]}")
    assert _FINAL in record.output or "read" in [tc.name for tc in record.tool_calls]


@pytest.mark.asyncio
async def test_fixture_is_called_2(workspace, install_model):
    """Debug test 2."""
    print("\nTest 2: Calling install_model...")
    install_model(read_then_finish(_NOTES, _FINAL))
    print("Test 2: install_model called")

    record = await run_agent_once("read the notes file", cwd=workspace)
    print(f"Test 2: record.output = {record.output[:50]}")
    assert _FINAL in record.output or "read" in [tc.name for tc in record.tool_calls]
