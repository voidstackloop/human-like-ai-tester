"""Realistic Human Error Patterns and Test Vectors."""

from typing import Dict, List

# Realistic personal names that reveal character encoding / validation bugs
REALISTIC_NAMES_WITH_QUIRKS: List[str] = [
    "Mary-Jane O'Connor",
    "José Ramón Peña",
    "Zoë Chloë St. John",
    "Dr. Arthur Conan Doyle, Jr.",
    "Björn Åkesson",
    "John Doe ",                # Trailing space
    "  Alice Smith",            # Leading space
    "Alexandre Dumas-Fils",
    "Null",                     # Famous name causing SQL / code bugs
    "Ng",                       # 2-letter last name (often blocked by min_length=3)
    "Wolfeschlegelsteinhausenbergerdorff", # Very long legal surname
]

# Realistic addresses filled by humans
REALISTIC_ADDRESS_ERRORS: List[str] = [
    "Apt 4B, 742 Evergreen Terrace",
    "123 Main St. #5",
    "PO Box 4501",
    "742 Evergreen Terr, Springfield, OR 97477", # Pasted full address into line 1
    "Baker Street 221B (Ring bell twice)",
]

# Phone number input variations commonly produced by humans
REALISTIC_PHONE_VARIANTS: List[str] = [
    "(555) 234-5678",
    "555-234-5678",
    "555.234.5678",
    "+1 (555) 234-5678",
    "5552345678",
    "1-555-234-5678",
    "(555)234-5678 ext 102",
    "555 234 5678",
]

# Date entries entered by humans
REALISTIC_DATE_ERRORS: List[str] = [
    "12/05/2026",        # Ambiguous MM/DD vs DD/MM
    "05-12-2026",
    "October 14, 2026",  # Natural language entered into strict field
    "14 Oct 2026",
    "2026/10/14",
    "10/14/26",          # 2-digit year
]

# Currency entries entered by humans
REALISTIC_CURRENCY_ERRORS: List[str] = [
    "$1,499.00",
    "$ 1499",
    "1,499.00",
    "1499.00 USD",
    "1.499,00 €",        # European comma decimal format
    "free",              # Natural language when price is 0
]

# Password copy/paste and caps-lock mishaps
REALISTIC_PASSWORD_QUIRKS: List[str] = [
    "hunter2 ",                 # Trailing space from sloppy select
    "HUNTER2",                  # Caps lock left on
    "hunter",                   # Truncated by bad double-click select
    " hunter2",                 # Leading space from password manager
    "hunter2\\t",               # Trailing tab
]

# Search-box input quirks
REALISTIC_SEARCH_QUIRKS: List[str] = [
    "iphnoe 15",                # Typo in product search
    "best coffe near me",       # Typo + local intent
    "WHAT IS MY ORDER STATUS",  # Accidental caps lock
    "laptop under $500 2024?",  # Natural question into keyword box
    "   red shoes   ",          # Padded paste
]

# Address-bar / URL input quirks
REALISTIC_URL_ERRORS: List[str] = [
    "example.com",              # Missing scheme
    "htp://example.com",        # Protocol typo
    "https:/example.com",       # Missing slash
    "example..com",             # Doubled dot
    "https://example.com ",     # Trailing space
]

# Credit-card entry variants
REALISTIC_CREDIT_CARD_VARIANTS: List[str] = [
    "4111 1111 1111 1111",
    "4111-1111-1111-1111",
    "4111111111111111",
    "4111 1111 1111 1111 ",     # Trailing space
]

# i18n / locale traps: same string, different meaning per locale
I18N_LOCALE_TRAPS: List[Dict[str, str]] = [
    {"input": "12/05/2026", "trap": "US reads Dec 5; EU reads 12 May. Reject or disambiguate?"},
    {"input": "1.499,00", "trap": "EU decimal comma vs US thousands separator."},
    {"input": "1,499.00", "trap": "US decimal dot vs EU thousands separator."},
    {"input": "São Paulo", "trap": "Latin-1 vs UTF-8 mojibake risk (SÃ£o Paulo)."},
    {"input": "山田太郎", "trap": "CJK width: truncation by bytes breaks graphemes."},
    {"input": "مرحبا بالعالم", "trap": "RTL text in LTR layout: alignment + cursor jumps."},
]

# Common mistakes humans make when submitting forms
FORM_INTERACTION_FLAWS: List[Dict[str, str]] = [
    {
        "id": "proximity_cancel_click",
        "description": "User accidentally clicks 'Cancel' or 'Reset' instead of 'Submit' because buttons are placed too close.",
        "prevention": "Visually de-emphasize cancel buttons and separate from primary submit."
    },
    {
        "id": "unnoticed_terms_checkbox",
        "description": "User misses the 'I agree to the terms' checkbox because it blends into the footer text.",
        "prevention": "Clear visual callout and scrolling error focus."
    },
    {
        "id": "unformatted_phone_rejection",
        "description": "System rejects phone number formatted with parentheses/dashes instead of sanitizing raw digits automatically.",
        "prevention": "Accept any standard phone format and strip non-digits server-side."
    },
    {
        "id": "double_click_duplicate_order",
        "description": "User double-clicks the purchase button because of network latency, resulting in duplicate transactions.",
        "prevention": "Immediately disable submit button on first click and display progress spinner."
    },
    {
        "id": "form_clear_on_validation_error",
        "description": "The page reloads and wipes out 10 fields because the user missed 1 required field.",
        "prevention": "Preserve all valid field states during re-render."
    },
    {
        "id": "offscreen_error_banner",
        "description": "Error banner appears at the very top of the page, but the user is scrolled down at the bottom submit button.",
        "prevention": "Auto-scroll viewport to the first erroneous input field."
    }
]

# Accessibility barriers keyboard/screen-reader users hit
ACCESSIBILITY_BARRIERS: List[Dict[str, str]] = [
    {
        "id": "missing_focus_ring",
        "description": "Keyboard-only user tabs through the form but cannot see which field is focused.",
        "prevention": "Never remove :focus-visible outlines; use a 2px+ high-contrast ring."
    },
    {
        "id": "icon_only_button",
        "description": "Screen reader announces 'button' with no name on an icon-only control.",
        "prevention": "Give every control an accessible name (aria-label or visible text)."
    },
    {
        "id": "modal_focus_trap_missing",
        "description": "Tab escapes a modal dialog into the background page; Escape does not close it.",
        "prevention": "Trap focus inside modals; close on Escape; return focus to the trigger."
    },
    {
        "id": "session_timeout_no_warning",
        "description": "Session expires mid-form with no warning; all typed data is lost on re-login.",
        "prevention": "Warn before timeout, offer extend, and preserve draft input."
    },
    {
        "id": "captcha_only_gate",
        "description": "Image-only CAPTCHA blocks screen-reader and low-vision users with no alternative.",
        "prevention": "Provide an audio or logic-based alternative path."
    },
]

# Mobile & touch friction vectors
MOBILE_TOUCH_FLAWS: List[Dict[str, str]] = [
    {
        "id": "thumb_unreachable_primary",
        "description": "Primary action sits top-right, unreachable for one-handed right-thumb use.",
        "prevention": "Place primary actions in the bottom half / thumb zone."
    },
    {
        "id": "keyboard_covers_submit",
        "description": "Soft keyboard covers the submit button; user cannot see errors below it.",
        "prevention": "Scroll focused field + submit above the keyboard; use visualViewport."
    },
    {
        "id": "orientation_state_loss",
        "description": "Rotating the phone wipes typed form data or restarts the flow.",
        "prevention": "Persist form state across configuration changes."
    },
    {
        "id": "rage_tap_duplicate",
        "description": "Sluggish button invites rage-taps that fire duplicate requests.",
        "prevention": "Debounce taps; disable during flight; show instant feedback."
    },
]

# Desktop GUI friction vectors
DESKTOP_GUI_FLAWS: List[Dict[str, str]] = [
    {
        "id": "window_resize_breaks_layout",
        "description": "Narrowing the window clips the submit button with no scroll affordance.",
        "prevention": "Responsive layout with min sizes + scrollable content regions."
    },
    {
        "id": "dialog_cancel_midway",
        "description": "Cancelling a file dialog mid-flow leaves a half-applied state with no undo.",
        "prevention": "Treat dialog cancel as atomic no-op with clear status copy."
    },
    {
        "id": "shortcut_collision",
        "description": "Ctrl+S triggers browser save instead of app save; user loses work.",
        "prevention": "Scope shortcuts to the app; confirm before destructive browser defaults."
    },
    {
        "id": "drag_drop_miss",
        "description": "Drop target too small; file lands outside and the import silently does nothing.",
        "prevention": "Large drop zone, hover highlight, and explicit error on missed drop."
    },
]

# API / GraphQL / webhook friction vectors
API_GRAPHQL_FLAWS: List[Dict[str, str]] = [
    {
        "id": "boolean_string_rejection",
        "description": "API 500s on {\"active\": \"true\"} instead of coercing or 400ing.",
        "prevention": "Coerce 'true'/'false' strings or return a precise 400."
    },
    {
        "id": "pagination_off_by_one",
        "description": "page=0 or page='2' returns 500 or wrong slice instead of normalized results.",
        "prevention": "Clamp/normalize page + limit; document 0- vs 1-based indexing."
    },
    {
        "id": "graphql_typo_no_hint",
        "description": "GraphQL typo'd field returns a raw stack trace instead of 'Did you mean X?'.",
        "prevention": "Sanitize GraphQL errors; suggest nearest field names."
    },
    {
        "id": "webhook_double_delivery",
        "description": "Retried webhook creates a duplicate side effect (double email/charge).",
        "prevention": "Idempotency keys on event IDs; dedupe within a window."
    },
]


def all_vectors() -> Dict[str, List]:
    """Return every test-vector collection keyed by category name."""
    return {
        "names": REALISTIC_NAMES_WITH_QUIRKS,
        "addresses": REALISTIC_ADDRESS_ERRORS,
        "phones": REALISTIC_PHONE_VARIANTS,
        "dates": REALISTIC_DATE_ERRORS,
        "currencies": REALISTIC_CURRENCY_ERRORS,
        "passwords": REALISTIC_PASSWORD_QUIRKS,
        "search": REALISTIC_SEARCH_QUIRKS,
        "urls": REALISTIC_URL_ERRORS,
        "credit_cards": REALISTIC_CREDIT_CARD_VARIANTS,
        "i18n_traps": I18N_LOCALE_TRAPS,
        "form_flaws": FORM_INTERACTION_FLAWS,
        "accessibility": ACCESSIBILITY_BARRIERS,
        "mobile": MOBILE_TOUCH_FLAWS,
        "desktop": DESKTOP_GUI_FLAWS,
        "api": API_GRAPHQL_FLAWS,
    }
