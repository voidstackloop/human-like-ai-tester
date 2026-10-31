"""Realistic Human Typo & Keystroke Slip Generator."""

import random
import re
from typing import Optional, Union

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

# Mobile autocorrect wrong-word substitutions (intended -> what autocorrect produced).
AUTOCORRECT_SWAPS = {
    "meeting": ["melting", "misting"],
    "definately": ["defiantly"],
    "definitely": ["defiantly"],
    "duck": ["luck", "tuck"],
    "well": ["we'll"],
    "ill": ["I'll"],
    "cant": ["can't", "cant"],
    "its": ["it's"],
    "your": ["you're"],
    "there": ["their", "they're"],
    "def": ["deg", "dec"],
    "test": ["text", "tent"],
    "code": ["coke", "cove"],
    "ship": ["shop", "sheep"],
    "demo": ["demon"],
    "lets": ["let's"],
    "dont": ["don't", "font"],
}

# Voice-transcription homophone confusions (spoken -> transcribed).
VOICE_HOMOPHONES = {
    "their": ["there", "they're"],
    "there": ["their", "they're"],
    "they're": ["their", "there"],
    "to": ["too", "two"],
    "too": ["to", "two"],
    "two": ["to", "too"],
    "your": ["you're"],
    "you're": ["your"],
    "its": ["it's"],
    "it's": ["its"],
    "for": ["four", "fore"],
    "four": ["for"],
    "by": ["buy", "bye"],
    "buy": ["by", "bye"],
    "right": ["write", "rite"],
    "write": ["right"],
    "here": ["hear"],
    "hear": ["here"],
    "new": ["knew"],
    "know": ["no"],
    "no": ["know"],
}

# ESL phonetic misspellings (correct -> common phonetic variant).
PHONETIC_SPELLINGS = {
    "through": ["tru", "troo"],
    "because": ["becouse", "becase"],
    "address": ["adress"],
    "phone": ["fone"],
    "enough": ["enouf"],
    "people": ["pipol"],
    "receipt": ["receit", "reciept"],
    "separate": ["seperate"],
    "definitely": ["definetly"],
    "tomorrow": ["tommorow"],
    "password": ["pasword"],
    "message": ["mesage"],
    "please": ["plese", "pls"],
    "thanks": ["thx", "thanx"],
    "really": ["realy"],
    "which": ["wich"],
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

    def format_currency_human_style(self, amount: Union[float, int]) -> str:
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

    # -- Enriched human-input vectors -------------------------------------

    def introduce_autocorrect_fail(self, text: str) -> str:
        """Simulate a mobile autocorrect wrong-word substitution.

        Swaps at most one known word for an autocorrect artifact; returns the
        original text unchanged when no known word is present.
        """
        words = text.split(" ")
        candidates = [i for i, w in enumerate(words) if w.lower().strip(".,!?") in AUTOCORRECT_SWAPS]
        if not candidates:
            return text
        idx = random.choice(candidates)
        core = words[idx].lower().strip(".,!?")
        words[idx] = random.choice(AUTOCORRECT_SWAPS[core])
        return " ".join(words)

    def introduce_voice_transcription_errors(self, text: str) -> str:
        """Simulate voice-dictation artifacts: homophone swaps, dropped
        capitalization and punctuation, occasional filler words."""
        words = text.split(" ")
        out = []
        for w in words:
            core = w.lower().strip(".,!?")
            if core in VOICE_HOMOPHONES and random.random() < 0.6:
                out.append(random.choice(VOICE_HOMOPHONES[core]))
            else:
                out.append(core)
        result = " ".join(out)
        if random.random() < 0.35:
            fillers = ["um", "uh", "like"]
            pos = random.randint(0, len(out))
            parts = result.split(" ")
            parts.insert(min(pos, len(parts)), random.choice(fillers))
            result = " ".join(parts)
        return result

    def introduce_phonetic_spelling(self, text: str) -> str:
        """Simulate ESL phonetic spelling for known words (adress, fone...)."""
        def _swap(match: "re.Match") -> str:
            word = match.group(0)
            variant = random.choice(PHONETIC_SPELLINGS[word.lower()])
            return variant.capitalize() if word[0].isupper() else variant

        pattern = re.compile(
            r"\b(" + "|".join(re.escape(k) for k in PHONETIC_SPELLINGS) + r")\b",
            re.IGNORECASE,
        )
        return pattern.sub(_swap, text)

    def corrupt_password_paste(self, password: str) -> str:
        """Simulate password-manager / copy-paste mishaps: trailing space,
        truncated last char (bad double-click select), or caps-lock inversion."""
        choices = ["trailing_space", "truncated", "caps_invert", "clean"]
        pick = random.choice(choices)
        if pick == "trailing_space":
            return password + " "
        elif pick == "truncated" and len(password) > 1:
            return password[:-1]
        elif pick == "caps_invert":
            return password.swapcase()
        return password

    def corrupt_url_bar(self, url: str) -> str:
        """Simulate human address-bar input: missing scheme, doubled dots,
        stray spaces, or protocol typos like htp://."""
        variants = [
            url.replace("https://", "").replace("http://", ""),
            url.replace("https://", "htp://").replace("http://", "htp://"),
            url.replace(".", "..", 1),
            f"{url} ",
            url.replace("https://", "https:/"),
        ]
        return random.choice(variants)

    def format_date_human_style(self, year: int, month: int, day: int) -> str:
        """Render one calendar date the way humans in different locales type it,
        including the ambiguous MM/DD vs DD/MM trap."""
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        name = month_names[max(1, min(12, month)) - 1]
        yy = f"{year % 100:02d}"
        styles = [
            f"{month:02d}/{day:02d}/{year}",      # US MM/DD/YYYY
            f"{day:02d}/{month:02d}/{year}",      # EU DD/MM/YYYY (ambiguous!)
            f"{year}-{month:02d}-{day:02d}",      # ISO
            f"{day:02d}-{month:02d}-{year}",      # EU dashes
            f"{name} {day}, {year}",              # Natural language
            f"{day} {name} {year}",               # Natural EU order
            f"{month}/{day}/{yy}",                # Lazy 2-digit year
        ]
        return random.choice(styles)

    def format_credit_card_human_style(self, digits: str) -> str:
        """Render card digits with human spacing/dash habits."""
        clean = "".join(ch for ch in digits if ch.isdigit())
        groups = [clean[i:i + 4] for i in range(0, len(clean), 4)]
        styles = [
            " ".join(groups),
            "-".join(groups),
            clean,
            " ".join(groups) + " ",
        ]
        return random.choice(styles)
