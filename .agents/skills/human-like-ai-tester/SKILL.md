---
name: human-like-ai-tester
description: >-
  Universal AI testing skill that tests ANY application type (Web, CLI, Desktop GUI, Mobile/Touch, REST/GraphQL APIs, Chatbots/Conversational AI, and File Ingestion Pipelines) exactly like an authentic human user. Simulates real-world human mistakes, typos, formatting idiosyncrasies, impatience, non-linear navigation, cognitive biases, and rage-clicks to uncover usability friction and silent failures. Now also covers accessibility (keyboard/screen-reader), i18n/locale traps, voice dictation, and autocorrect failures.
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
- They rely on **autocorrect and voice dictation** that silently rewrite their words (`meeting` → `melting`, `their` → `there`).
- They read **literally and locally**: `12/05/2026` means December 5 in the US but 12 May in Europe.

This skill equips an AI agent to **completely shed robotic perfection** and test **ALL application types** as an authentic, imperfect human.

---

## What's New in v0.2.0

- **8 personas** (was 5): added Priya (Accessibility Navigator), Mateo (Non-Native Speaker), Zoe (Impatient Teen).
- **Desktop GUI + Mobile testers**: heuristic audits (button proximity, resize clipping, thumb reach, keyboard overlap, rotation wipes, deep links, permissions) with printable manual walkthrough scripts.
- **New input vectors**: autocorrect fails, voice-transcription homophones, ESL phonetic spelling, password-paste mishaps, URL-bar typos, locale-aware dates, credit-card spacing.
- **Deeper API/CLI/chat/file coverage**: boolean-as-string, pagination misuse, GraphQL typo fields, webhook double-delivery, Ctrl-C handling, colloquial prompt answers, 10 conversational patterns (voice, code-switching, ALL-CAPS), TSV + CSV robustness validation.
- **Severity rubric + frustration guide + session workflow** (sections 5–6) and a **multi-persona `audit` command** producing one merged report.

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

Cross-cutting passes (apply to every paradigm): **Accessibility** (keyboard-only, screen reader) and **i18n/Locale** (date/decimal ambiguity, accented/CJK/RTL text).

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

### 6. The Accessibility Navigator (Keyboard-Only / Screen Reader)
- **Typing Cadence**: 35 WPM | **Typo Rate**: 6% | **Patience Threshold**: 5.0 seconds.
- **Cognitive Style**: Tabs through everything; depends on visible focus rings, real labels, heading order. Trapped by modals without focus traps, icon-only buttons, silent session timeouts.
- **Primary Paradigms**: Web portals, desktop GUIs, any form-heavy flow.

### 7. The Non-Native Speaker (ESL / Locale Confusion)
- **Typing Cadence**: 30 WPM | **Typo Rate**: 20% (phonetic) | **Patience Threshold**: 4.5 seconds.
- **Cognitive Style**: Reads idioms literally, mixes DD/MM vs MM/DD and comma/dot decimals, spells phonetically (`adress`, `fone`, `becouse`). Misreads terse error codes.
- **Primary Paradigms**: Web forms, chatbots, file imports with locale-formatted data.

### 8. The Impatient Teen (Mobile-Native / Autocorrect Relier)
- **Typing Cadence**: 70 WPM (thumb) | **Typo Rate**: 22% (autocorrect artifacts) | **Patience Threshold**: 1.0 seconds.
- **Cognitive Style**: Trusts autocorrect blindly, screenshots instead of reading, back-swipes rather than navigating. Abandons any flow that stalls, demands login, or shows a wall of text.
- **Primary Paradigms**: Mobile apps, social/checkout flows, chatbots.

**Recommended persona sets per paradigm** (see `personas_for_paradigm()`):
web → rushed, novice, accessibility · mobile → rushed, teen, non-native · desktop → novice, accessibility, power · cli → power, fatigued, non-native · api → power, fatigued, explorer · chat → novice, non-native, teen · file → fatigued, non-native, explorer.

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
4. **Back-Button & Navigation Resilience**:
   - Fill half a form, press browser Back, then Forward: is every keystroke intact?
   - Close a modal via backdrop-click and Escape: is focus returned to the trigger?

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
4. **Interruption & Paste Accidents**:
   - Press Ctrl-C during a long run: clean `Aborted.` + exit 130, or a raw traceback / ignored signal?
   - Pass empty-string args and stray `--` from a bad paste: usage error, or crash?

### C. REST, GraphQL & Backend APIs
1. **Type Coercion & Permissiveness**:
   - Send numeric values as strings: `{"count": "42"}`.
   - Send booleans as strings: `{"active": "true"}`.
   - Verify: Does the API gracefully coerce the type or return a clean 400 Bad Request, or does it trigger an unhandled 500 Internal Server Error?
2. **Routing & Header Variations**:
   - Test endpoints with and without trailing slashes (`/users` vs `/users/`).
   - Send authorization tokens without the `Bearer ` prefix.
   - Send extra unexpected metadata fields: `{"id": 1, "custom_tag": "test"}`.
3. **Pagination, GraphQL & Webhooks**:
   - Guess `page=0`, `page=two`, `limit=999999`: normalized results or 500s?
   - Typo a GraphQL field: sanitized `Did you mean users?` error, or a leaked stack trace?
   - Deliver the same webhook event twice: exactly-once effect, or duplicate emails/charges?

### D. Conversational AI & Chatbots
1. **Vague & Fragmented Requests**:
   - Submit ambiguous complaints: "It doesn't work", "Fix my account".
   - Check if the assistant gently clarifies or fails with a rigid error.
2. **Mid-Sentence Reversals**:
   - "Cancel my booking. Wait, actually don't cancel it, change the time to 5pm."
   - Check whether the assistant caught the negation.
3. **Premature Submissions**:
   - Submit an incomplete sentence: "When I click on the settings tab it".
4. **Voice, Multilingual & Emotional Users**:
   - Dictate by voice: homophone garble (`there account... hear me out`) with no punctuation — still understood?
   - Code-switch mid-request ("I need ayuda with mi factura") — handled or rejected?
   - Shout in ALL CAPS after failures: does the reply acknowledge frustration before troubleshooting?
   - Reference an unattached screenshot ("see pic") — does the bot ask for the missing image?

### E. File & Data Ingestion Pipelines
1. **Excel Artifacts**:
   - Provide CSV files prefixed with the UTF-8 Byte Order Mark (`\ufeff`).
   - Include mixed delimiters (semicolons in European locale rows).
2. **Trailing Quirks**:
   - Add trailing blank lines, spaces in column headers (` Name `, ` Amount `).
   - Unescaped commas in text fields: `Bob Jones, Jr., bob@example.com`.
3. **Headers, TSV & Validation**:
   - Vary header case (`Name` vs `NAME` vs `name`): is the importer case-brittle?
   - Feed tab-delimited (TSV) paste-from-Excel exports and human-edited JSON with trailing commas.
   - Run `validate-file` on real customer samples to enumerate traps before they hit prod.

### F. Desktop GUI Applications
1. **Proximity & Misclick Risk**: Is Cancel/Reset ≥40px from Submit and visually de-emphasized? A fatigued slip must not nuke a finished form.
2. **Resize Robustness**: Narrow the window to 1024px then 800px mid-flow: primary actions stay reachable, never silently clipped.
3. **Dialog Atomicity**: Change values in a file/settings dialog, press Cancel: NOTHING is applied, with clear status copy.
4. **Shortcuts & Drop Targets**: No collisions with OS/browser defaults; missed drag-drops fail loudly with a large highlighted zone.

### G. Mobile & Touch Applications
1. **Thumb Zone**: Primary actions live in the bottom half; top-corner placement fails one-handed use.
2. **Keyboard Overlap**: With the soft keyboard open, submit + inline errors stay visible (scroll above `visualViewport`).
3. **Rotation & Deep Links**: Rotating preserves every keystroke; cold-start deep links land on the content, not home.
4. **Permissions & Rage-Taps**: Pre-prompt rationale in plain language; denial keeps the flow usable; sluggish buttons debounce to exactly one request.

### H. Accessibility & i18n Pass (all paradigms)
1. **Keyboard-Only Run**: Tab/Shift+Tab through the whole flow — visible focus everywhere, logical order, modals trap focus and close on Escape.
2. **Screen-Reader Sanity**: Every control announces a name (no bare "button"); errors are announced inline, not color-only.
3. **Timeout Kindness**: Warn before session expiry, offer extend, preserve drafts — never wipe input on re-login.
4. **Locale Traps**: Enter `12/05/2026`, `1.499,00`, `São Paulo`, `山田太郎`, RTL text — rejected with guidance, never mojibake or silent misparse.

---

## 4. Universal Human-Tester Tooling in This Workspace

The project includes an executable simulation engine located in `~/projects/human-like-ai-tester/`:

```bash
# View available human personas (8)
python3 -m human_tester.cli personas

# Test a CLI tool as a human user
python3 -m human_tester.cli test-cli git --flags --version --help --work-tree

# Test a Web application or form
python3 -m human_tester.cli test-web http://localhost:3000 --form-endpoint /submit

# Test an API endpoint with human developer mistakes (+ GraphQL typo check)
python3 -m human_tester.cli test-api http://localhost:8000 --endpoint /api/v1/orders --graphql-endpoint /graphql

# Desktop / Mobile heuristic audits (print findings + manual walkthrough)
python3 -m human_tester.cli test-desktop "MyApp" --cancel-distance-px 12 --clipped-at 800
python3 -m human_tester.cli test-mobile "MyApp" --action-position top-right --keyboard-covered

# Multi-persona sweep with one merged report
python3 -m human_tester.cli audit http://localhost:3000 --form-endpoint /submit --endpoint /api/orders -o audit.md

# Generate human conversational test streams for Chatbots (+ voice mode, reply eval)
python3 -m human_tester.cli test-chat --persona rushed_commuter
python3 -m human_tester.cli test-chat --persona impatient_teen --voice --reply "Error 500. Try again."

# Simulate typos / voice / autocorrect / phonetic variants of any text
python3 -m human_tester.cli simulate "Lets plan a meeting tomorrow" --voice --autocorrect --phonetic

# Generate messy human files (CSV/TSV/JSON) and audit real ones
python3 -m human_tester.cli generate-file csv --mixed --output messy_human_data.csv
python3 -m human_tester.cli validate-file messy_human_data.csv

# Run an end-to-end live demo with built-in flawed mock app
python3 -m human_tester.cli demo
```

---

## 5. Severity Rubric & Frustration Index

Assign every finding one severity:

| Severity | Meaning | Examples |
| :--- | :--- | :--- |
| 🔴 CRITICAL | User blocked, data lost/corrupted, or money duplicated | wiped inputs, double charges, rotation wipe, 500 on string `"42"` |
| 🟡 FRICTION | User slowed, confused, or rage-clicking but can finish | strict phone rejection, no typo hint, keyboard-covered submit |
| 🔵 MODERATE | Papercut: noticeable, easy workaround | missing `Did you mean`, off-screen banner, caps-lock password fail |
| 🟢 DELIGHT | Human-proofing worth celebrating (rare) | autocorrect-tolerant search, graceful colloquial `yeah` handling |

Frustration index (0–100, tracked by `CognitiveEngine`): 0–24 calm, 25–49 annoyed, 50–74 highly frustrated, 75–100 abandonment imminent. Score +35 for wiped inputs, +20 for cryptic errors, +15 per rage-click burst, +12/sec past the patience threshold, −10 per successful retry (learning relief).

---

## 6. Session Workflow

Every human-like test session follows five steps:

1. **Scope**: name the target (URL / command / endpoint / flow) and pick the paradigm(s) from §1.
2. **Adopt**: choose 1–3 personas from §2 (use the recommended sets; always include one low-patience and one low-skill persona).
3. **Execute**: run the §3 procedures for your paradigm — live via §4 tooling plus the desktop/mobile manual scripts where no driver exists. Narrate the inner monologue ("Did it submit or is it hanging?").
4. **Score**: record severity per §5 and sync the frustration index from the cognitive engine.
5. **Report**: conclude with the §7 audit report including the prioritized remediation plan.

---

## 7. Output Format: Human Usability & Robustness Report

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
