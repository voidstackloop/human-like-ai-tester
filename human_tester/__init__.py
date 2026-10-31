"""Human-Like AI Tester - Real-World Human User Simulation Package."""

__version__ = "0.1.0"

from .personas import (
    Persona,
    get_persona,
    list_personas,
    RUSHED_COMMUTER,
    TECH_NOVICE,
    CYNICAL_POWER_USER,
    FATIGUED_WORKER,
    CURIOUS_EXPLORER,
)
from .typo_engine import TypoEngine
from .cognitive_engine import CognitiveEngine
from .reporter import AuditReporter

__all__ = [
    "Persona",
    "get_persona",
    "list_personas",
    "RUSHED_COMMUTER",
    "TECH_NOVICE",
    "CYNICAL_POWER_USER",
    "FATIGUED_WORKER",
    "CURIOUS_EXPLORER",
    "TypoEngine",
    "CognitiveEngine",
    "AuditReporter",
]
