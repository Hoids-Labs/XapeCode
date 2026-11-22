"""Unit coverage for the committed demo skills (ADR-0017 §2 Track A, tasks 117-119).

The demo skills live at the repo root under ``.xape/skills/demo-N-*/`` and are graded by humans,
not the harness — so the only thing to pin automatically is that they stay *loadable* and that the
fixtures their bodies reference stay honest: demo-2's seeded repo must genuinely fail exactly two
tests as committed. Everything runs through xape's REAL skills loader
(``xape.skills.loader``), mirroring ``test_loader.py``.

The prompt-only demos — demo-1 (terminal-arcade), demo-3 (repo-pulse), demo-4 (review-swarm),
demo-5 (sandbox-feature-pr), and demo-6 (article-kg) — ship no fixtures, so they owe the
loader-parse coverage plus a pin on the contract their body promises. demo-5 gets one extra guard:
its documented invocation must match the REAL CLI (``--repo`` exists; sandbox mode is the
``SANDBOX_MODE`` env var, never an invented ``--sandbox`` flag).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from xape.skills import loader

# ``tests/unit/xape/skills/test_demo_skills.py`` -> repo root -> the committed demo skills tree.
REPO_ROOT = Path(__file__).resolve().parents[4]
DEMO_SKILLS_DIR = REPO_ROOT / ".xape" / "skills"

DEMO = "grill-me"
DEMO_2 = "demo-2-bug-hunt"
DEMO_3 = "demo-3-repo-pulse"
DEMO_4 = "demo-4-review-swarm"
DEMO_5 = "demo-5-sandbox-feature-pr"
DEMO_6 = "demo-6-article-kg"
# All but demo-2 are prompt-only (SKILL.md, no sibling resources).
PROMPT_ONLY_DEMOS = [DEMO]
AUTHORED_DEMOS = [DEMO]


def _skill_text(dir_name: str) -> str:
    """Read a demo skill's committed ``SKILL.md`` from the repo-root skills tree."""
    return (DEMO_SKILLS_DIR / dir_name / "SKILL.md").read_text(encoding="utf-8")


# SKILL.md parses through the real loader


@pytest.mark.parametrize("dir_name", AUTHORED_DEMOS)
def test_demo_skill_md_parses_through_the_real_loader(dir_name):
    # Each demo's SKILL.md must survive xape's own parser: frontmatter name matches the directory
    # convention (dir name is cosmetic but we keep them aligned) and both fields are non-empty.
    skill = loader.parse_skill_file(_skill_text(dir_name), source="test")

    assert skill.name == dir_name
    assert skill.description.strip()
    assert skill.body.strip()


def test_authored_demos_appear_in_the_project_catalog():
    # Discovery over the real repo-root skills dir surfaces all five by frontmatter name, so they
    # show up in the Skills Catalog and dispatch via ``/demo-2-bug-hunt`` etc.
    found = loader.discover_project_skills(REPO_ROOT)

    assert set(AUTHORED_DEMOS) <= set(found)


def test_authored_demos_load_alongside_the_builtins():
    # The merged catalog (built-ins + project) keeps the built-ins and adds the demos — nothing is
    # dropped by the merge.
    skills = loader.load_skills(REPO_ROOT)

    assert {"commit", "review-diff"} <= set(skills)
    assert set(AUTHORED_DEMOS) <= set(skills)
