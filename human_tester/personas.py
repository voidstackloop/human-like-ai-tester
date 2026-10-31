"""User Persona Catalog for Authentic Human Simulation."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


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

PERSONA_REGISTRY: Dict[str, Persona] = {
    RUSHED_COMMUTER.id: RUSHED_COMMUTER,
    TECH_NOVICE.id: TECH_NOVICE,
    CYNICAL_POWER_USER.id: CYNICAL_POWER_USER,
    FATIGUED_WORKER.id: FATIGUED_WORKER,
    CURIOUS_EXPLORER.id: CURIOUS_EXPLORER,
}


def get_persona(persona_id: str) -> Persona:
    """Retrieve persona by key, default to RUSHED_COMMUTER."""
    clean_id = persona_id.lower().replace("-", "_")
    return PERSONA_REGISTRY.get(clean_id, RUSHED_COMMUTER)


def list_personas() -> List[Persona]:
    """Return all available persona definitions."""
    return list(PERSONA_REGISTRY.values())
