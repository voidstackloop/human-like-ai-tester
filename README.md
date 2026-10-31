# 🧑 Universal Human-Like AI Tester: Multi-Paradigm Human Simulation

> An AI agent skill and autonomous test simulation engine that tests **ANY application type** (Web, CLI, Desktop GUI, Mobile/Touch, APIs, Conversational AI, and File Ingestion) completely like an authentic human being—making genuine typos, formatting errors, non-linear navigation, rage-clicks, and mental model misunderstandings to uncover real-world usability friction, silent failures, and validation flaws.

---

## 🌟 Why Human-Like Testing?

Traditional automated testing (deterministic unit tests, synthetic bots, happy-path crawlers) only verifies whether software works when used **flawlessly**.

In reality, authentic human users:
- **Do not read instructions** or tooltips.
- **Make physical typos** (adjacent keyboard keys, omitted letters, finger bounces).
- **Format data idiosyncratically** (typing `(555) 234-5678` or `555.234.5678` into strict digit fields, typing `$1,500.00` into numeric price fields).
- **Get impatient** and rage-click buttons if feedback takes > 1.5 seconds, risking double-submission bugs.
- **Navigate non-linearly**: relying on browser Back buttons, pressing Escape, closing modals by clicking backdrops, and abandoning forms mid-flow.
- **Make mental model mistakes**: passing string `"25"` instead of integer `25` to APIs, omitting quotes around paths with spaces in CLIs, or reversing their intent mid-sentence in chatbots.

---

## 🎯 Universal Coverage: The 7 Program Paradigms

This skill is 100% program-agnostic and explicitly covers all seven software paradigms:

| Paradigm | Target Types | Human Mistakes & Behaviors Simulated |
| :--- | :--- | :--- |
| **1. Web & SPAs** | Web apps, portals, eCommerce, SaaS | Rapid double-clicks on slow submits, phone/address formatting quirks, losing state on validation errors, back-button reliance. |
| **2. CLI & Terminal** | Shell tools, developer CLIs, scripts | Flag typos (`--hlpe`, `--verboose`), unquoted spaces in paths (`my folder/file.txt`), hitting Enter on empty prompts, colloquial answers (`yeah`, `yep`). |
| **3. Desktop GUI** | Electron, Qt, native desktop apps | Accidental clicks on close/cancel due to proximity, window resizing breaking layout, cancelling file dialogs midway. |
| **4. Mobile & Touch** | iOS, Android, responsive web | Thumb reachability issues, soft keyboard covering submit buttons, rage-tapping sluggish buttons, orientation flips. |
| **5. APIs & Services** | REST, JSON, GraphQL, Webhooks | String vs integer types (`"42"` vs `42`), trailing slashes (`/items` vs `/items/`), missing `Bearer ` prefix, extra payload fields. |
| **6. Conversational AI** | Chatbots, agents, voice assistants | Vague requests ("it doesn't work"), mid-sentence mind reversals, slang, fragmented sentences sent prematurely. |
| **7. Data Ingestion** | CSV/Excel pipelines, batch imports | UTF-8 Excel BOM marks (`\ufeff`), mixed delimiters (comma vs semicolon), trailing blank rows, unescaped commas in names. |

---

## 🧑 Persona Catalog

The simulation engine includes 5 pre-configured psychographic personas:

1. **Alex (Rushed Commuter)**: Mobile-first, high typo rate (28%), very low patience (1.8s), rage clicks unresponsive buttons, skims headers only.
2. **Margaret (Senior / Tech Novice)**: Desktop user, slow typing (22 WPM), high formatting error rate (65%), heavily relies on browser Back button, fears breaking things.
3. **David (Cynical Power User)**: Keyboard-driven (110 WPM), low tolerance for friction (1.2s), tests boundary values, flags layout reflows and latency.
4. **Sam (Fatigued Data Clerk)**: End-of-shift worker, prone to transpositions (`teh`), misses required fields below the fold, accidentally clicks Cancel due to button proximity.
5. **Elena (Curious Explorer)**: Enters accented characters (`Renée`, `O'Connor`), emojis in names, resizes windows mid-flow, tests unusual combinations.

---

## 🚀 Quickstart & CLI Commands

### 1. View Available Personas
```bash
python3 -m human_tester.cli personas
```

### 2. Test a Web Application or Form
```bash
python3 -m human_tester.cli test-web http://localhost:3000 --form-endpoint /submit --persona rushed_commuter
```

### 3. Test a CLI Tool
```bash
python3 -m human_tester.cli test-cli git --flags=version,help --persona rushed_commuter
```

### 4. Test an API Endpoint
```bash
python3 -m human_tester.cli test-api http://localhost:8000 --endpoint /api/users --persona cynical_power_user
```

### 5. Generate Human Conversational Prompts for Chatbots
```bash
python3 -m human_tester.cli test-chat --persona rushed_commuter
```

### 6. Generate Messy Human Files (CSV / JSON)
```bash
python3 -m human_tester.cli generate-file csv --mixed --output messy_human_data.csv
```

### 7. Run the Live Demo (Self-Contained Mock App with UX Flaws)
```bash
python3 -m human_tester.cli demo
```

---

## 📂 Project Architecture

```
human-like-ai-tester/
├── SKILL.md                          # Official Agent Skill definition (Frontmatter + deep human behavioral protocol)
├── README.md                         # Project documentation
├── pyproject.toml                    # Python package specification
├── requirements.txt                  # Dependencies
├── human_tester/
│   ├── __init__.py
│   ├── cli.py                        # Unified multi-paradigm CLI
│   ├── personas.py                   # Psychographic user profiles & metrics
│   ├── typo_engine.py                # QWERTY physical key slips, omissions, transpositions
│   ├── cognitive_engine.py           # Reading times, hesitation pauses, frustration tracking, rage clicks
│   ├── error_patterns.py             # Human formatting variants (phone, currency, names)
│   ├── reporter.py                   # Usability & Robustness Audit Report generator
│   ├── agent_prompts.py              # LLM system prompts for agentic human testing
│   ├── mock_target_app.py            # Lightweight test app with intentional real-world UX flaws
│   └── paradigms/
│       ├── __init__.py
│       ├── cli_tester.py             # CLI application tester
│       ├── api_tester.py             # REST/API service tester
│       ├── web_tester.py             # Web & Mobile application tester
│       ├── chat_tester.py            # Conversational AI & Chatbot tester
│       └── file_tester.py            # Messy human file generator
└── tests/
    └── test_human_tester.py          # Unit tests covering all paradigms
```

---

## 🧪 Running Unit Tests

```bash
python3 -m unittest discover -s tests
```
