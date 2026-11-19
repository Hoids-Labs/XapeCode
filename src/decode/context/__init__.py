"""Context engineering: conversation persistence + compaction (ADR-0002 §9, ADR-0006).

:mod:`xape.context.session_log` is the replayable JSONL log ``xape --resume`` seeds from;
:mod:`xape.context.compaction` owns the compaction primitives.
"""

from __future__ import annotations

from xape.context.session_log import (
    SessionLog,
    SessionSummary,
    list_sessions,
    load,
    load_latest,
    resolve_session,
)

__all__ = [
    "SessionLog",
    "SessionSummary",
    "list_sessions",
    "load",
    "load_latest",
    "resolve_session",
]
