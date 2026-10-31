"""Realistic Human Typo & Keystroke Slip Generator."""

import random
from typing import Optional

# Standard US QWERTY physical keyboard adjacency map
QWERTY_ADJACENT = {
    'q': ['w', 'a', '1', '2'],
    'w': ['q', 'e', 's', 'a', '2', '3'],
    'e': ['w', 'r', 'd', 's', '3', '4'],
    'r': ['e', 't', 'f', 'd', '4', '5'],
    't': ['r', 'y', 'g', 'f', '5', '6'],
    'y': ['t', 'u', 'h', 'g', '6', '7'],
    'u': ['y', 'i', 'j', 'h', '7', '8'],
    'i': ['u', 'o', 'k', 'j', '8', '9'],
    'o': ['i', 'p', 'l', 'k', '9', '0'],
    'p': ['o', 'l', '0', '-'],
    'a': ['q', 'w', 's', 'z'],
    's': ['a', 'w', 'e', 'd', 'x', 'z'],
    'd': ['s', 'e', 'r', 'f', 'c', 'x'],
    'f': ['d', 'r', 't', 'g', 'v', 'c'],
    'g': ['f', 't', 'y', 'h', 'b', 'v'],
    'h': ['g', 'y', 'u', 'j', 'n', 'b'],
    'j': ['h', 'u', 'i', 'k', 'm', 'n'],
    'k': ['j', 'i', 'o', 'l', 'm'],
    'l': ['k', 'o', 'p'],
    'z': ['a', 's', 'x'],
    'x': ['z', 's', 'd', 'c'],
    'c': ['x', 'd', 'f', 'v'],
    'v': ['c', 'f', 'g', 'b'],
    'b': ['v', 'g', 'h', 'n'],
    'n': ['b', 'h', 'j', 'm'],
    'm': ['n', 'j', 'k'],
    '1': ['2', 'q'],
    '2': ['1', '3', 'w', 'q'],
    '3': ['2', '4', 'e', 'w'],
    '4': ['3', '5', 'r', 'e'],
    '5': ['4', '6', 't', 'r'],
    '6': ['5', '7', 'y', 't'],
    '7': ['6', '8', 'u', 'y'],
    '8': ['7', '9', 'i', 'u'],
    '9': ['8', '0', 'o', 'i'],
    '0': ['9', '-', 'p', 'o'],
    '-': ['0', '=', 'p'],
}

COMMON_DOMAIN_TYPOS = {
    "gmail.com": ["gmai.com", "gmail.con", "gmial.com", "gmaill.com", "gamil.com"],
    "yahoo.com": ["yaho.com", "yahooo.com", "yahoo.con", "yaho.co"],
    "outlook.com": ["outlok.com", "outloo.com", "outlook.con"],
    "hotmail.com": ["hotmial.com", "hotmai.com", "hotmail.con"],
    "company.com": ["copmany.com", "compnay.com"],
}


class TypoEngine:
    """Simulates real-world human keystroke errors and formatting deviations."""

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def apply_adjacent_key_slip(self, char: str) -> str:
        """Replace char with physically adjacent key."""
        lower = char.lower()
        if lower in QWERTY_ADJACENT:
            replacement = random.choice(QWERTY_ADJACENT[lower])
            return replacement.upper() if char.isupper() else replacement
        return char

    def introduce_transposition(self, text: str) -> str:
        """Invert two adjacent characters, e.g. 'the' -> 'teh'."""
        if len(text) < 2:
            return text
        idx = random.randint(0, len(text) - 2)
        chars = list(text)
        chars[idx], chars[idx + 1] = chars[idx + 1], chars[idx]
        return "".join(chars)

    def introduce_omission(self, text: str) -> str:
        """Skip a character accidentally, e.g. 'committee' -> 'comittee'."""
        if len(text) < 3:
            return text
        idx = random.randint(0, len(text) - 1)
        return text[:idx] + text[idx + 1:]

    def introduce_fat_finger(self, text: str) -> str:
        """Double-strike a key due to finger bounce, e.g. 'book' -> 'boook'."""
        if not text:
            return text
        idx = random.randint(0, len(text) - 1)
        return text[:idx] + text[idx] + text[idx:]

    def introduce_typos(self, text: str, error_rate: float = 0.15) -> str:
        """Apply a mixture of realistic human typing slips based on error_rate."""
        if not text or error_rate <= 0.0:
            return text

        chars = list(text)
        result = []
        i = 0
        while i < len(chars):
            ch = chars[i]
            if random.random() < error_rate and ch.isalpha():
                choice = random.random()
                if choice < 0.50:
                    # Adjacent key hit
                    result.append(self.apply_adjacent_key_slip(ch))
                elif choice < 0.70 and i + 1 < len(chars):
                    # Transposition
                    result.append(chars[i + 1])
                    result.append(ch)
                    i += 1
                elif choice < 0.85:
                    # Omission (skip character)
                    pass
                else:
                    # Fat finger duplicate
                    result.append(ch)
                    result.append(ch)
            else:
                result.append(ch)
            i += 1

        res = "".join(result)
        return res if res else text

    def corrupt_email(self, email: str, error_rate: float = 0.20) -> str:
        """Introduce common human mistakes into email addresses."""
        if "@" not in email:
            return email
        username, domain = email.split("@", 1)

        roll = random.random()
        if roll < error_rate * 0.5:
            # Trailing or leading space from copy paste
            return f" {email} "
        elif roll < error_rate:
            # Domain typo
            domain_clean = domain.strip().lower()
            if domain_clean in COMMON_DOMAIN_TYPOS:
                typo_domain = random.choice(COMMON_DOMAIN_TYPOS[domain_clean])
                return f"{username}@{typo_domain}"
            else:
                # Omit dot or transpose
                return f"{username}@{self.introduce_typos(domain, 0.25)}"
        return email

    def format_phone_human_style(self, raw_digits: str) -> str:
        """Take raw 10 digits and return how different humans write phone numbers."""
        digits = "".join(ch for ch in raw_digits if ch.isdigit())
        if len(digits) < 10:
            digits = digits.ljust(10, '0')
        area = digits[:3]
        prefix = digits[3:6]
        line = digits[6:10]

        styles = [
            f"({area}) {prefix}-{line}",      # US standard formatted
            f"{area}-{prefix}-{line}",        # Hyphenated
            f"{area}.{prefix}.{line}",        # Dotted
            f"+1 ({area}) {prefix}-{line}",   # Country code with parenthesis
            f"1-{area}-{prefix}-{line}",      # Leading 1
            f"{area} {prefix} {line}",        # Space delimited
            f"({area}){prefix}{line}",        # Squeezed parenthesis
            f"{area}-{prefix}-{line} ext 14", # Extra extension text
        ]
        return random.choice(styles)

    def format_currency_human_style(self, amount: float or int) -> str:
        """Format currency how users typically enter it instead of raw float."""
        val = float(amount)
        styles = [
            f"${val:,.2f}",      # $1,250.00
            f"${int(val)}",      # $1250
            f"{val:,.2f}",       # 1,250.00
            f"{val:.2f} USD",    # 1250.00 USD
            f"$ {val:,.2f}",     # $ 1,250.00
            f" {val:.2f} ",      # " 1250.00 " with spaces
        ]
        return random.choice(styles)

    def add_clipboard_quirks(self, text: str) -> str:
        """Add clipboard paste artifacts like unexpected whitespaces."""
        patterns = [
            f" {text}",          # Leading space
            f"{text} ",          # Trailing space
            f"  {text}  ",       # Double spaces
            f"{text}\t",         # Trailing tab
        ]
        return random.choice(patterns)
