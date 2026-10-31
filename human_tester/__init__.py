"""Human-Like AI Tester - Real-World Human User Simulation Package."""

__version__ = "0.2.0"

from .personas import (
    Persona,
    get_persona,
    list_personas,
    personas_for_paradigm,
    describe_persona,
    RUSHED_COMMUTER,
    TECH_NOVICE,
    CYNICAL_POWER_USER,
    FATIGUED_WORKER,
    CURIOUS_EXPLORER,
    ACCESSIBILITY_NAVIGATOR,
    NON_NATIVE_SPEAKER,
    IMPATIENT_TEEN,
)
from .typo_engine import TypoEngine
from .cognitive_engine import CognitiveEngine
from .reporter import AuditReporter

__all__ = [
    "Persona",
    "get_persona",
    "list_personas",
    "personas_for_paradigm",
    "describe_persona",
    "RUSHED_COMMUTER",
    "TECH_NOVICE",
    "CYNICAL_POWER_USER",
    "FATIGUED_WORKER",
    "CURIOUS_EXPLORER",
    "ACCESSIBILITY_NAVIGATOR",
    "NON_NATIVE_SPEAKER",
    "IMPATIENT_TEEN",
    "TypoEngine",
    "CognitiveEngine",
    "AuditReporter",
]
