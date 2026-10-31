# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- `human-tester --version` flag and `python -m human_tester` module shortcut.
- `audit --json-output` for machine-readable reports in CI pipelines.
- `examples/python_api_example.py` showing library (non-CLI) usage.
- MIT `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`.
- GitHub Actions CI (tests on Python 3.9–3.13, ruff, package build check).
- `tests/test_cli_stability.py`: guards for all 12 subcommands, `--version`,
  `--help` coverage, and CLI error exit codes.

### Changed

- `validate-file` on a missing/unreadable path now prints a clear error and
  exits with code 2 instead of a traceback.
- Package version is now defined once in `human_tester/__init__.py`.
- Expanded `pyproject.toml` metadata (license, classifiers, keywords, dev extras).

### Fixed

- Corrected the `format_currency_human_style` type annotation and the reporter
  metrics annotation.
- Removed dead assignments and unused imports (ruff-clean).

## [0.2.0]

- 8 personas: added Accessibility Navigator, Non-Native Speaker, Impatient Teen.
- New Desktop GUI and Mobile heuristic testers with manual walkthrough scripts.
- New input vectors: autocorrect fails, voice-transcription homophones, ESL
  phonetic spelling, password-paste mishaps, URL-bar typos, locale-aware dates,
  credit-card spacing.
- Deeper API/CLI/chat/file coverage: boolean-as-string, pagination misuse,
  GraphQL typo fields, webhook double-delivery, Ctrl-C handling, colloquial
  prompt answers, TSV + CSV robustness validation.
- Multi-persona `audit` command producing one merged, deduplicated report.
- Severity rubric, frustration guide, and session workflow in `SKILL.md`.
