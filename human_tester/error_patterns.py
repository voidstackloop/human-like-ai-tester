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
