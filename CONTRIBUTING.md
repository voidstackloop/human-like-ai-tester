# Contributing to human-like-ai-tester

Thanks for helping make software behave for real humans. This project keeps a
small, stable surface: additive improvements are welcome, breaking CLI changes
are not (see below).

## Setup

Requires Python 3.9+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Checks (run before every PR)

```bash
python -m unittest discover -s tests   # full suite, ~10s
python -m ruff check human_tester tests # lint gate (also runs in CI)
```

New behavior needs a test in `tests/` using the existing `unittest` style.
Bug fixes should add the smallest regression test that fails without the fix.

## Pull request rules

1. **Keep the CLI stable.** All 12 subcommands and their flags are covered by
   `tests/test_cli_stability.py`. Add flags, never rename or remove them.
2. **Keep it dependency-free.** The runtime package has zero mandatory
   dependencies — that is a feature. New optional integrations belong behind
   extras or imports that degrade gracefully.
3. **Keep it network-free in tests.** Live HTTP is only exercised by the
   self-contained `demo` command against its own mock server.
4. **Update docs with behavior.** New flags need README + `--help` coverage;
   user-facing changes need a `CHANGELOG.md` entry under Unreleased.

## Project layout

- `human_tester/` — library + CLI (`cli.py`, `personas.py`, engines, `reporter.py`)
- `human_tester/paradigms/` — one tester per program paradigm
- `tests/` — `unittest` suite (also runnable under pytest)
- `examples/` — guided tour (`quickstart.sh`), API example, sample report
- `SKILL.md` — the agent-skill definition; keep it in sync with CLI changes

## Release checklist (maintainers)

1. Bump `__version__` in `human_tester/__init__.py` (single source of truth).
2. Move Unreleased entries to a new `CHANGELOG.md` section.
3. Tag `vX.Y.Z`, build with `python -m build`, check with `twine check dist/*`.
