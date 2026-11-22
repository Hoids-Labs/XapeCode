"""Project memory: read ``AGENTS.md`` / ``MEMORY.md`` and inject them into the prompt (ADR-0002 §8).

:mod:`xape.memory.files` discovers the files (ancestor ``AGENTS.md`` walk + the single
harness ``cwd/.xape/MEMORY.md``); :mod:`xape.memory.service` assembles and caps them;
:mod:`xape.memory.extract` writes the on-exit summary back. The factory's dynamic
``@agent.instructions`` hook calls ``assemble_memory`` at prompt-build time, so edits take
effect on the next run.
"""
