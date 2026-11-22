"""``xape remote`` — the Modal Headless App and the ``xape`` subcommands that launch it (ADR-0020).

Launch-vs-execute split: the laptop only launches (:mod:`xape.remote.cli`), Modal executes
(:mod:`xape.remote.app`, deployed once with ``xape remote deploy``). Nothing here is imported by
the REPL or by ``xape run``; ``modal`` itself is imported only by the app module and, lazily,
inside the subcommands that talk to the deployment.
"""
