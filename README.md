# 🧑 Human-Like AI Tester

[![PyPI version](https://img.shields.io/pypi/v/human-like-ai-tester)](https://pypi.org/project/human-like-ai-tester/)
[![Python 3.9+](https://img.shields.io/pypi/pyversions/human-like-ai-tester)](https://pypi.org/project/human-like-ai-tester/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/voidstackloop/human-like-ai-tester/actions/workflows/ci.yml/badge.svg)](https://github.com/voidstackloop/human-like-ai-tester/actions/workflows/ci.yml)

Test **any application type** — Web, CLI, Desktop GUI, Mobile, APIs,
Conversational AI, File Ingestion — like an authentic human being: genuine
typos, formatting quirks, rage-clicks, non-linear navigation, and mental-model
mistakes that uncover real-world friction, silent failures, and validation flaws.

Zero runtime dependencies. Eight psychographic personas. One merged report.

## 30-second demo

```bash
pip install human-like-ai-tester
human-tester demo        # self-contained mock app with intentional UX flaws
```

Prefer a tour? `bash examples/quickstart.sh` walks the whole engine in ~2 minutes,
and [`examples/python_api_example.py`](examples/python_api_example.py) shows library usage.

## Why human-like testing?

Traditional testing verifies software used **flawlessly**. Real users:

- **Don't read instructions** — they skim headers and miss below-the-fold fields.
- **Make physical typos** — adjacent keys, omitted letters, finger bounces (`teh`).
- **Format idiosyncratically** — `(555) 234-5678` in digit-only fields, `$1,500.00`
  in numeric price fields.
- **Get impatient** — rage-clicking buttons after ~1.5s of silence, risking
  double submissions.
- **Navigate non-linearly** — Back buttons, Escape, backdrop clicks, mid-flow
  abandonment.
- **Think differently than your schema** — string `"25"` instead of int `25`,
  unquoted CLI paths with spaces, mind-changing mid-sentence in chatbots.
- **Trust autocorrect and voice dictation** — silently rewritten words — and read
  dates/numbers through their own locale (`12/05/2026` is Dec 5 in the US,
  12 May in Europe).

## Install

```bash
pip install human-like-ai-tester        # from PyPI
# or from source:
git clone <your-fork> && cd human-like-ai-tester
pip install -e .[dev]                   # dev extras: ruff, build, twine, coverage
```

Requires Python 3.9+. The runtime package has **zero mandatory dependencies**.

## Quickstart

```bash
human-tester personas                  # list the 8 simulation personas
human-tester simulate "Lets meet tomorrow" --voice --autocorrect --phonetic
human-tester test-web http://localhost:3000 --form-endpoint /submit
human-tester audit http://localhost:3000 --form-endpoint /submit \
  --endpoint /api/orders -o audit.md --json-output audit.json
```

## The 7 program paradigms

| Paradigm | Targets | Human behaviors simulated |
| :--- | :--- | :--- |
| **Web & SPAs** | Portals, eCommerce, SaaS | Double-clicks on slow submits, phone/address quirks, state loss on errors, Back-button reliance |
| **CLI & Terminal** | Shell tools, dev CLIs | Flag typos (`--hlpe`), unquoted spaces, bare Enter, colloquial answers (`yeah`) |
| **Desktop GUI** | Electron, Qt, native | Misclicks from button proximity, resize breakage, cancelled dialogs |
| **Mobile & Touch** | iOS, Android, responsive | Thumb reach, keyboard-covered submits, rage-taps, orientation flips |
| **APIs & Services** | REST, GraphQL, webhooks | String-vs-int types, trailing slashes, missing `Bearer `, extra fields |
| **Conversational AI** | Chatbots, agents, voice | Vague complaints, mid-sentence reversals, slang, premature sends |
| **Data Ingestion** | CSV/TSV/JSON pipelines | Excel BOM, mixed delimiters, blank rows, unescaped commas |

Cross-cutting every paradigm: **Accessibility** (keyboard-only, screen reader)
and **i18n/Locale** (date/decimal ambiguity, accented/CJK/RTL text).

## Personas

| ID | Persona | Signature behavior |
| :--- | :--- | :--- |
| `rushed_commuter` | Alex, Rushed Commuter | 28% typos, 1.8s patience, rage-taps |
| `tech_novice` | Margaret, Senior / Tech Novice | 65% formatting errors, Back-button reliant |
| `cynical_power_user` | David, Power User | 110 WPM keyboard-only, boundary values |
| `fatigued_worker` | Sam, Fatigued Data Clerk | Transpositions, below-the-fold misses |
| `curious_explorer` | Elena, Explorer | Emojis, accented chars, window resizing |
| `accessibility_navigator` | Priya, A11y Navigator | Keyboard + screen reader, focus traps |
| `non_native_speaker` | Mateo, ESL User | Locale confusion, phonetic spelling |
| `impatient_teen` | Zoe, Impatient Teen | Autocorrect reliance, 1.0s patience, back-swipes |

## CLI reference

| Command | Purpose |
| :--- | :--- |
| `personas` | List personas |
| `simulate TEXT` | Humanize text (`--voice --autocorrect --phonetic --clipboard`) |
| `test-web URL` | Page load, form formatting, double-submit, state loss |
| `test-cli CMD` | Help discovery, flag typos, paths, Ctrl-C, whitespace |
| `test-api URL` | Slashes, type coercion, booleans, pagination, webhooks, GraphQL |
| `test-chat` | Generate human/voice prompts, evaluate assistant replies |
| `test-desktop APP` | Button proximity, resize clipping, dialogs, shortcuts, drag-drop |
| `test-mobile APP` | Thumb reach, keyboard overlap, rotation, deep links, permissions |
| `generate-file` | Messy CSV/TSV/JSON fixtures for ingestion tests |
| `validate-file PATH` | Audit a real CSV for ingestion traps (exit 2 if unreadable) |
| `audit URL` | Multi-persona web+API sweep, one deduplicated report (`-o`, `--json-output`) |
| `demo` | Live end-to-end run against the built-in flawed mock app |

Every command supports `--persona ID` (and `--help`). Run `human-tester --version`
to print the version.

## Python API

```python
from human_tester import TypoEngine, get_persona

persona = get_persona("rushed_commuter")
typos = TypoEngine(seed=42)
print(typos.introduce_typos("Lets plan a meeting", error_rate=persona.typo_rate))
print(typos.format_phone_human_style("5551234567"))
```

See [`examples/python_api_example.py`](examples/python_api_example.py) for the full
tour (personas, cognition, chat vectors, file audits, reports), and
[`examples/sample_audit_report.md`](examples/sample_audit_report.md) for an annotated report.

## Agent skill

`SKILL.md` is the agent-skill definition: behavioral protocol, severity rubric,
frustration guide, and session workflow for AI agents that test as humans.
Keep it in sync with CLI changes.

## Project architecture

```text
human-like-ai-tester/
├── SKILL.md                  # Agent skill definition (behavioral protocol)
├── README.md                 # This file
├── pyproject.toml            # Package metadata (version lives in human_tester/__init__.py)
├── LICENSE                   # MIT
├── CONTRIBUTING.md           # Setup, checks, PR rules
├── CHANGELOG.md              # Release history
├── human_tester/
│   ├── __init__.py           # Public API + __version__
│   ├── __main__.py           # `python -m human_tester` shortcut
│   ├── cli.py                # 12-command CLI
│   ├── personas.py           # 8 psychographic profiles
│   ├── typo_engine.py        # Typos, autocorrect, voice, phonetic, locale formats
│   ├── cognitive_engine.py   # Reading, hesitation, frustration, rage clicks
│   ├── error_patterns.py     # Formatting variants + a11y/i18n/mobile/API vectors
│   ├── reporter.py           # Markdown + JSON audit reports
│   ├── agent_prompts.py      # LLM prompts for agentic human testing
│   ├── mock_target_app.py    # Flawed demo app for `demo`
│   └── paradigms/            # web, cli, api, chat, file, desktop, mobile testers
├── examples/
│   ├── quickstart.sh         # 2-minute guided tour
│   ├── python_api_example.py # Library usage (network-free)
│   ├── sample_audit_report.md
│   └── manual_desktop_mobile_script.md
├── tests/                    # unittest suite (core, enrichment, CLI stability)
└── .github/                  # CI (3.9–3.13, ruff, build) + issue/PR templates
```

## Tests

```bash
python -m unittest discover -s tests   # 71 tests, network-free, ~10s
python -m ruff check human_tester tests # lint gate
```

## Contributing

Contributions welcome — new personas, behaviors, and paradigms especially.
Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) first. The short version:
keep the CLI backward compatible, keep runtime dependencies at zero, and add a
test with every behavior change.

## License

MIT — see [LICENSE](LICENSE).
