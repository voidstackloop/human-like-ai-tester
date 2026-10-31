"""User Persona Catalog for Authentic Human Simulation."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Persona:
    """Psychographic user profile controlling AI behavior during testing."""

    id: str
    name: str
    archetype: str
    description: str
    wpm: int                          # Words per minute typing speed
    typo_rate: float                  # Probability of typo per typed word/input (0.0 - 1.0)
    patience_seconds: float           # Max delay tolerated before rage clicking or abandoning
    reading_depth: str                # 'skims', 'selective', 'thorough'
    rage_click_probability: float     # Chance of rapid multi-clicking when slow
    miss_below_fold_rate: float       # Chance of ignoring content requiring scroll
    back_button_preference: float     # Chance of pressing browser back instead of in-app navigation
    format_error_rate: float          # Chance of entering phone/money/date in natural language
    unintended_tab_drop_rate: float   # Chance of leaving mid-flow
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "archetype": self.archetype,
            "description": self.description,
            "wpm": self.wpm,
            "typo_rate": self.typo_rate,
            "patience_seconds": self.patience_seconds,
            "reading_depth": self.reading_depth,
            "rage_click_probability": self.rage_click_probability,
            "miss_below_fold_rate": self.miss_below_fold_rate,
            "back_button_preference": self.back_button_preference,
            "format_error_rate": self.format_error_rate,
            "tags": self.tags,
        }


# Standard Personas
RUSHED_COMMUTER = Persona(
    id="rushed_commuter",
    name="Alex (Rushed Commuter)",
    archetype="Distracted Mobile User",
    description="One-handed smartphone user rushing to catch a train. Inattentive, skips all instructions, highly prone to fat-fingered taps, and will rage-tap unresponsive buttons.",
    wpm=45,
    typo_rate=0.28,
    patience_seconds=1.8,
    reading_depth="skims",
    rage_click_probability=0.75,
    miss_below_fold_rate=0.45,
    back_button_preference=0.60,
    format_error_rate=0.35,
    unintended_tab_drop_rate=0.20,
    tags=["mobile", "high-error", "impatient", "rage-clicker"]
)

TECH_NOVICE = Persona(
    id="tech_novice",
    name="Margaret (Senior / Tech Novice)",
    archetype="Anxious Non-Technical User",
    description="Unfamiliar with modern web patterns. Clicks static text labels expecting input focus, gets trapped by modals, writes natural language in strict fields, and fears breaking things.",
    wpm=22,
    typo_rate=0.12,
    patience_seconds=6.0,
    reading_depth="selective",
    rage_click_probability=0.15,
    miss_below_fold_rate=0.55,
    back_button_preference=0.85,
    format_error_rate=0.65,
    unintended_tab_drop_rate=0.05,
    tags=["desktop", "hesitant", "formatting-errors", "back-button-reliant"]
)

CYNICAL_POWER_USER = Persona(
    id="cynical_power_user",
    name="David (Cynical Power User)",
    archetype="Keyboard-Driven Specialist",
    description="Types at blazing speed, uses Tab/Shift+Tab exclusively, dislikes mouse interactions, attempts boundary values, and instantly spots UX friction and visual layout reflows.",
    wpm=110,
    typo_rate=0.03,
    patience_seconds=1.2,
    reading_depth="skims",
    rage_click_probability=0.40,
    miss_below_fold_rate=0.05,
    back_button_preference=0.20,
    format_error_rate=0.05,
    unintended_tab_drop_rate=0.10,
    tags=["desktop", "keyboard-nav", "fast", "boundary-tester"]
)

FATIGUED_WORKER = Persona(
    id="fatigued_worker",
    name="Sam (Fatigued Data Clerk)",
    archetype="Exhausted Repetitive Worker",
    description="Tired at the end of an 8-hour shift. Makes transposition errors, misses required checkboxes below the fold, accidentally clicks 'Cancel' due to proximity, and takes long pauses.",
    wpm=38,
    typo_rate=0.18,
    patience_seconds=4.0,
    reading_depth="selective",
    rage_click_probability=0.25,
    miss_below_fold_rate=0.35,
    back_button_preference=0.30,
    format_error_rate=0.25,
    unintended_tab_drop_rate=0.15,
    tags=["desktop", "fatigued", "transpositions", "abandonment"]
)

CURIOUS_EXPLORER = Persona(
    id="curious_explorer",
    name="Elena (Curious Explorer)",
    archetype="Unpredictable Real-World Explorer",
    description="Enters emojis into name fields, tries multi-line inputs, pastes accented foreign characters, resizes the browser window mid-task, and tests what happens when clicking background elements.",
    wpm=60,
    typo_rate=0.08,
    patience_seconds=3.0,
    reading_depth="thorough",
    rage_click_probability=0.30,
    miss_below_fold_rate=0.10,
    back_button_preference=0.40,
    format_error_rate=0.40,
    unintended_tab_drop_rate=0.05,
    tags=["exploratory", "unicode", "edge-case", "resizer"]
)

ACCESSIBILITY_NAVIGATOR = Persona(
    id="accessibility_navigator",
    name="Priya (Accessibility Navigator)",
    archetype="Keyboard-Only / Screen-Reader User",
    description="Navigates by Tab/Shift+Tab and screen reader alone. Depends on visible focus rings, real labels, logical heading order, and skippable nav. Trapped by modals without focus traps, icon-only buttons, and session timeouts with no warning.",
    wpm=35,
    typo_rate=0.06,
    patience_seconds=5.0,
    reading_depth="thorough",
    rage_click_probability=0.10,
    miss_below_fold_rate=0.60,
    back_button_preference=0.30,
    format_error_rate=0.15,
    unintended_tab_drop_rate=0.08,
    tags=["desktop", "keyboard-nav", "screen-reader", "accessibility"]
)

NON_NATIVE_SPEAKER = Persona(
    id="non_native_speaker",
    name="Mateo (Non-Native Speaker)",
    archetype="ESL User with Locale Confusion",
    description="Reads English literally and translates mentally. Trips on idioms ('a chip off the old block'), mixes DD/MM vs MM/DD dates and comma-vs-dot decimals, and spells phonetically (adress, becouse). Patient but misreads terse error codes.",
    wpm=30,
    typo_rate=0.20,
    patience_seconds=4.5,
    reading_depth="selective",
    rage_click_probability=0.20,
    miss_below_fold_rate=0.40,
    back_button_preference=0.50,
    format_error_rate=0.55,
    unintended_tab_drop_rate=0.12,
    tags=["desktop", "mobile", "i18n", "locale-confusion", "phonetic-spelling"]
)

IMPATIENT_TEEN = Persona(
    id="impatient_teen",
    name="Zoe (Impatient Teen)",
    archetype="Mobile-Native Autocorrect Relier",
    description="Thumb-types fast on mobile, trusts autocorrect blindly, screenshots instead of reading, and back-swipes rather than using in-app nav. Zero patience: abandons any flow that stalls, asks for login, or shows a wall of text.",
    wpm=70,
    typo_rate=0.22,
    patience_seconds=1.0,
    reading_depth="skims",
    rage_click_probability=0.85,
    miss_below_fold_rate=0.50,
    back_button_preference=0.70,
    format_error_rate=0.30,
    unintended_tab_drop_rate=0.35,
    tags=["mobile", "impatient", "autocorrect", "rage-clicker", "abandonment"]
)

PERSONA_REGISTRY: Dict[str, Persona] = {
    RUSHED_COMMUTER.id: RUSHED_COMMUTER,
    TECH_NOVICE.id: TECH_NOVICE,
    CYNICAL_POWER_USER.id: CYNICAL_POWER_USER,
    FATIGUED_WORKER.id: FATIGUED_WORKER,
    CURIOUS_EXPLORER.id: CURIOUS_EXPLORER,
    ACCESSIBILITY_NAVIGATOR.id: ACCESSIBILITY_NAVIGATOR,
    NON_NATIVE_SPEAKER.id: NON_NATIVE_SPEAKER,
    IMPATIENT_TEEN.id: IMPATIENT_TEEN,
}

# Recommended personas per paradigm (ids into PERSONA_REGISTRY).
PARADIGM_PERSONA_MAP: Dict[str, List[str]] = {
    "web": ["rushed_commuter", "tech_novice", "accessibility_navigator"],
    "mobile": ["rushed_commuter", "impatient_teen", "non_native_speaker"],
    "desktop": ["tech_novice", "accessibility_navigator", "cynical_power_user"],
    "cli": ["cynical_power_user", "fatigued_worker", "non_native_speaker"],
    "api": ["cynical_power_user", "fatigued_worker", "curious_explorer"],
    "chat": ["tech_novice", "non_native_speaker", "impatient_teen"],
    "file": ["fatigued_worker", "non_native_speaker", "curious_explorer"],
}


def get_persona(persona_id: str) -> Persona:
    """Retrieve persona by key, default to RUSHED_COMMUTER."""
    clean_id = persona_id.strip().lower().replace("-", "_").replace(" ", "_")
    return PERSONA_REGISTRY.get(clean_id, RUSHED_COMMUTER)


def list_personas() -> List[Persona]:
    """Return all available persona definitions."""
    return list(PERSONA_REGISTRY.values())


def personas_for_paradigm(paradigm: str) -> List[Persona]:
    """Return recommended personas for a paradigm key (web, mobile, desktop,
    cli, api, chat, file). Falls back to the full catalog for unknown keys."""
    key = paradigm.strip().lower()
    ids = PARADIGM_PERSONA_MAP.get(key)
    if not ids:
        return list_personas()
    return [PERSONA_REGISTRY[i] for i in ids if i in PERSONA_REGISTRY]


def describe_persona(persona_id: str) -> str:
    """One-line human summary of a persona for CLI output and prompts."""
    p = get_persona(persona_id)
    return (
        f"{p.name} [{p.archetype}] — {p.wpm} WPM, "
        f"{int(p.typo_rate * 100)}% typos, {p.patience_seconds}s patience, "
        f"reads: {p.reading_depth}"
    )
