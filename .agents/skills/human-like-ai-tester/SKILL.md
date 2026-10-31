---
name: human-like-ai-tester
description: >-
  Universal AI testing skill that tests ANY application type (Web, CLI, Desktop GUI, Mobile/Touch, REST/GraphQL APIs, Chatbots/Conversational AI, and File Ingestion Pipelines) exactly like an authentic human user. Simulates real-world human mistakes, typos, formatting idiosyncrasies, impatience, non-linear navigation, cognitive biases, and rage-clicks to uncover usability friction and silent failures.
---

# Universal Human-Like AI Tester: Multi-Paradigm Human Simulation Skill

Traditional automated testing (unit tests, deterministic end-to-end scripts, synthetic bots) verifies whether software works when used **flawlessly**.

Real human users never interact with software flawlessly:
- They **skim text** and ignore instructions, tooltips, and disclaimers.
- They make **physical typos** (adjacent keyboard keys, omitted letters, finger bounces).
- They enter **idiosyncratic data** (entering `(555) 234-5678` when only digits are supported, or typing `$1,500.00` in numeric price fields).
- They get **impatient** when an interface pauses for > 1.5 seconds, rage-clicking buttons and triggering duplicate requests.
- They navigate **non-linearly**: relying on browser Back buttons, pressing Escape, closing modals by clicking backgrounds, and opening multiple tabs.
- They make **mental model mistakes**: guessing CLI flags, forgetting quotes around paths with spaces, or sending strings instead of integers in API calls.

This skill equips an AI agent to **completely shed robotic perfection** and test **ALL application types** as an authentic, imperfect human.

---

## 1. Universal Coverage: The 7 Program Paradigms

This skill is program-agnostic and explicitly covers all seven major software paradigms:

| Paradigm | Target Types | Human Mistakes & Behaviors Simulated |
| :--- | :--- | :--- |
| **1. Web & SPAs** | Web apps, portals, eCommerce, SaaS | Rapid double-clicks, phone/address formatting quirks, losing state on validation errors, back-button reliance. |
| **2. CLI & Terminal** | Shell tools, developer CLIs, scripts | Flag typos (`--hlpe`, `--verboose`), unquoted spaces in paths (`my folder/file.txt`), hitting Enter on empty prompts. |
| **3. Desktop GUI** | Electron, Qt, native desktop apps | Accidental clicks on close/cancel due to proximity, window resizing breaking layout, cancelling file dialogs midway. |
| **4. Mobile & Touch** | iOS, Android, responsive web | Thumb reachability issues, soft keyboard covering submit buttons, rage-tapping sluggish buttons, orientation flips. |
| **5. APIs & Services** | REST, JSON, GraphQL, Webhooks | String vs integer types (`"42"` vs `42`), trailing slashes (`/items` vs `/items/`), missing `Bearer ` prefix, extra payload fields. |
| **6. Conversational AI** | Chatbots, agents, voice assistants | Vague requests ("it doesn't work"), mid-sentence mind reversals, slang, fragmented sentences sent prematurely. |
| **7. Data Ingestion** | CSV/Excel pipelines, batch imports | UTF-8 Excel BOM marks (`\ufeff`), mixed delimiters (comma vs semicolon), trailing blank rows, unescaped commas in names. |

---

## 2. Universal Human Personas

Before testing any program, adopt one of these psychographic profiles:

### 1. The Rushed Commuter (Mobile / High Speed, High Error)
- **Typing Cadence**: 45 WPM | **Typo Rate**: 25–30% | **Patience Threshold**: 1.8 seconds.
- **Cognitive Style**: Skims only prominent text. Taps submit rapidly if response isn't instant (rage clicker).
- **Primary Paradigms**: Mobile apps, web checkout flows, short CLI commands.

### 2. The Tech Novice / Anxious Senior
- **Typing Cadence**: 22 WPM | **Typo Rate**: 12% | **Patience Threshold**: 6.0 seconds.
- **Cognitive Style**: Enters natural language into structured fields ("twelve" instead of `12`). Clicks static labels. Relies heavily on the Back button. Easily confused by modals and technical error codes.
- **Primary Paradigms**: Web portals, Desktop GUIs, conversational interfaces.

### 3. The Cynical Power User
- **Typing Cadence**: 110 WPM | **Typo Rate**: 3% | **Patience Threshold**: 1.2 seconds.
- **Cognitive Style**: Uses `Tab`, `Shift+Tab`, and keyboard shortcuts exclusively. Dislikes slow animations. Tests CLI flags, URL parameters, and boundary conditions.
- **Primary Paradigms**: Developer CLIs, APIs, desktop power tools, data ingestion.

### 4. The Fatigued Data Clerk
- **Typing Cadence**: 38 WPM | **Typo Rate**: 18% | **Patience Threshold**: 4.0 seconds.
- **Cognitive Style**: Mental fatigue leads to transposition slips (`teh`, swapped numbers: `1985` -> `1958`). Accidental clicks on "Cancel" because it sits right next to "Submit".
- **Primary Paradigms**: Internal web forms, data entry grids, file batch imports.

### 5. The Curious Explorer
- **Typing Cadence**: 60 WPM | **Typo Rate**: 8% | **Patience Threshold**: 3.0 seconds.
- **Cognitive Style**: Tests unusual inputs: names with accents (`Renée`, `O'Connor`), emojis in text fields, resizing windows mid-flow, pressing Ctrl+C during processing.
- **Primary Paradigms**: All applications.

---

## 3. Paradigm-Specific Testing Procedures

### A. Web & Mobile Applications
1. **Patience & Rage-Click Check**:
   - If an action takes > 1.5 seconds without immediate visual feedback, send 3–5 rapid clicks within 400ms.
   - Verify: Does the application lock the button, show a spinner, or permit duplicate orders/records?
2. **Human Input Idiosyncrasies**:
   - Enter formatted phone numbers: `(555) 234-5678` or `555.234.5678`.
   - Enter currency with symbols: `$1,499.00`.
   - Paste clipboard values with leading or trailing whitespace: `" John Doe "`.
3. **Error Recovery & State Preservation**:
   - Intentionally fail 1 field in a 10-field form.
   - Verify: Does the page preserve the other 9 fields, or does it cruelly wipe out everything?
   - Does the viewport auto-scroll to the first error, or is the error hidden off-screen?

### B. CLI & Terminal Applications
1. **Discoverability & Help**:
   - Run `--help`, `-h`, `help`, and `-?`. Check if error output suggests commands when mistyped.
2. **Flag & Subcommand Typos**:
   - Introduce subtle slips: `--verboose`, `--hlpe`, `--forcee`, `chekcout`.
   - Verify: Does the CLI provide a friendly "Did you mean ...?" suggestion or exit with an unhelpful error?
3. **Argument & Path Quirks**:
   - Pass paths with unquoted spaces: `my project folder/input.txt`.
   - Hit `Enter` on required interactive prompts without typing anything.
   - Answer interactive prompts with colloquial language: `yeah`, `yep`, `nah`, `sure`.

### C. REST, GraphQL & Backend APIs
1. **Type Coercion & Permissiveness**:
   - Send numeric values as strings: `{"count": "42"}`.
   - Send booleans as strings: `{"active": "true"}`.
   - Verify: Does the API gracefully coerce the type or return a clean 400 Bad Request, or does it trigger an unhandled 500 Internal Server Error?
2. **Routing & Header Variations**:
   - Test endpoints with and without trailing slashes (`/users` vs `/users/`).
   - Send authorization tokens without the `Bearer ` prefix.
   - Send extra unexpected metadata fields: `{"id": 1, "custom_tag": "test"}`.

### D. Conversational AI & Chatbots
1. **Vague & Fragmented Requests**:
   - Submit ambiguous complaints: "It doesn't work", "Fix my account".
   - Check if the assistant gently clarifies or fails with a rigid error.
2. **Mid-Sentence Reversals**:
   - "Cancel my booking. Wait, actually don't cancel it, change the time to 5pm."
   - Check whether the assistant caught the negation.
3. **Premature Submissions**:
   - Submit an incomplete sentence: "When I click on the settings tab it".

### E. File & Data Ingestion Pipelines
1. **Excel Artifacts**:
   - Provide CSV files prefixed with the UTF-8 Byte Order Mark (`\ufeff`).
   - Include mixed delimiters (semicolons in European locale rows).
2. **Trailing Quirks**:
   - Add trailing blank lines, spaces in column headers (` Name `, ` Amount `).
   - Unescaped commas in text fields: `Bob Jones, Jr., bob@example.com`.

---

## 4. Universal Human-Tester Tooling in This Workspace

The project includes an executable simulation engine located in `~/projects/human-like-ai-tester/`:

```bash
# View available human personas
python3 -m human_tester.cli personas

# Test a CLI tool as a human user
python3 -m human_tester.cli test-cli git --flags --version --help --work-tree

# Test a Web application or form
python3 -m human_tester.cli test-web http://localhost:3000 --form-endpoint /submit

# Test an API endpoint with human developer mistakes
python3 -m human_tester.cli test-api http://localhost:8000 --endpoint /api/v1/orders

# Generate human conversational test streams for Chatbots
python3 -m human_tester.cli test-chat --persona rushed_commuter

# Generate messy human files (CSV/JSON) for data pipeline testing
python3 -m human_tester.cli generate-file csv --output messy_human_data.csv

# Run an end-to-end live demo with built-in flawed mock app
python3 -m human_tester.cli demo
```

---

## 5. Output Format: Human Usability & Robustness Report

Every test session must conclude with a structured markdown audit report:

```markdown
# 🧑 Human-Centric Usability & Robustness Audit Report

## 1. Executive Summary
- **Target Application**: [App / URL / CLI Command / API / Pipeline]
- **Tested Persona**: [e.g. Alex (Rushed Commuter)]
- **Frustration Index**: [0.0 - 100.0%]
- **Overall Verdict**: [PASS / HIGH HUMAN FRICTION / CRITICAL USABILITY BLOCKER]

## 2. Findings Matrix
| Severity | Category | Finding | Human Action | System Reaction | Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 CRITICAL | Idempotency | Double-Submit Order Duplication | Rage-clicked 'Pay' 3x | Created duplicate charges | Disable button on click |
| 🟡 FRICTION | Validation | Strict Phone Rejection | Entered `(555) 123-4567` | Rejected: digits only | Auto-strip formatting |
| 🔵 MODERATE | CLI Guidance| No Typo Suggestion | Typed `--verboose` | Hard crash, no hint | Add 'Did you mean' |

## 3. Prioritized Developer Remediation Plan
1. [Highest priority fixes to prevent human user abandonment or data corruption]
```
