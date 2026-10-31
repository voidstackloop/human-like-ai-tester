"""Cognitive Simulation: Reading times, hesitation, frustration, and rage clicking."""

import random
import time
from typing import Dict, List, Tuple
from .personas import Persona


class CognitiveEngine:
    """Models human mental pace, cognitive load, frustration, and impatience."""

    def __init__(self, persona: Persona):
        self.persona = persona
        self.frustration_score = 0.0  # 0.0 (calm) to 100.0 (furious / task abandoned)
        self.action_history: List[Dict] = []

    def get_frustration_level(self) -> str:
        """Categorize current emotional frustration."""
        if self.frustration_score < 25.0:
            return "Calm / Cooperative"
        elif self.frustration_score < 50.0:
            return "Mildly Annoyed"
        elif self.frustration_score < 75.0:
            return "Highly Frustrated"
        else:
            return "Rage / Abandonment Imminent"

    def calculate_reading_delay_seconds(self, word_count: int) -> float:
        """Estimate how long this persona pauses to read on-screen text."""
        # Average adult reading speed ~200-250 wpm
        if self.persona.reading_depth == "skims":
            # Only skims headers (~500+ wpm equivalent, max 1.5 seconds)
            effective_words = min(word_count, 15)
            seconds = (effective_words / 450.0) * 60.0
        elif self.persona.reading_depth == "selective":
            effective_words = min(word_count, 45)
            seconds = (effective_words / 220.0) * 60.0
        else:
            # Thorough reading
            seconds = (word_count / 180.0) * 60.0

        # Add random human variance +/- 25%
        jitter = random.uniform(0.75, 1.25)
        return round(max(0.2, seconds * jitter), 2)

    def calculate_typing_delay_seconds(self, text_length: int) -> float:
        """Calculate human typing duration based on persona WPM."""
        # Standard assumption: 5 characters per word
        words = max(1.0, text_length / 5.0)
        base_seconds = (words / max(10, self.persona.wpm)) * 60.0
        jitter = random.uniform(0.85, 1.30)
        return round(base_seconds * jitter, 2)

    def calculate_hesitation_delay(self, complexity: str = "medium") -> float:
        """Pause before making a decision or clicking."""
        complexity_multipliers = {
            "low": 0.5,
            "medium": 1.0,
            "high": 2.2,
        }
        multiplier = complexity_multipliers.get(complexity, 1.0)
        base = 1.0 / (self.persona.wpm / 40.0)
        delay = random.uniform(0.4, 1.8) * base * multiplier
        return round(min(5.0, max(0.2, delay)), 2)

    def record_event(self, event_type: str, details: str, penalty: float = 0.0) -> Dict:
        """Log an interaction event and adjust frustration level."""
        self.frustration_score = min(100.0, max(0.0, self.frustration_score + penalty))
        entry = {
            "timestamp": time.time(),
            "event_type": event_type,
            "details": details,
            "penalty": penalty,
            "current_frustration": round(self.frustration_score, 1),
            "state": self.get_frustration_level(),
        }
        self.action_history.append(entry)
        return entry

    def trigger_rage_click_check(self, response_time_seconds: float) -> Tuple[bool, int, List[float]]:
        """Check if user loses patience and rage-clicks the button.
        Returns: (did_rage_click, click_count, click_intervals_ms)
        """
        if response_time_seconds > self.persona.patience_seconds:
            # Frustration increases significantly with slow UI
            penalty = (response_time_seconds - self.persona.patience_seconds) * 12.0
            self.record_event(
                "UI_HANG",
                f"Response took {response_time_seconds:.2f}s (patience: {self.persona.patience_seconds}s)",
                penalty=penalty,
            )

            if random.random() < self.persona.rage_click_probability:
                # User rage clicks 3 to 6 times
                click_count = random.randint(3, 6)
                # Rapid successive clicks between 80ms and 240ms apart
                intervals = [round(random.uniform(80.0, 240.0), 1) for _ in range(click_count - 1)]
                self.record_event(
                    "RAGE_CLICK",
                    f"Rage clicked button {click_count} times due to delayed response",
                    penalty=15.0,
                )
                return True, click_count, intervals

        return False, 1, []

    def handle_validation_error(self, cleared_inputs: bool = False, obscure_message: bool = False) -> str:
        """Simulate human reaction to form validation failures."""
        penalty = 10.0
        details = []

        if cleared_inputs:
            # One of the most frustrating things in web design
            penalty += 35.0
            details.append("System wiped out user's input fields on error!")

        if obscure_message:
            penalty += 20.0
            details.append("Error message is vague or technical (e.g. 'Invalid submission')")

        self.record_event("VALIDATION_ERROR", "; ".join(details) or "Validation failed", penalty=penalty)

        if self.frustration_score > 75.0:
            return "User is fed up, gives up, and is about to close the tab."
        elif self.frustration_score > 40.0:
            return "User sighs, attempts 1 fix, but is getting annoyed."
        else:
            return "User calmly reads the error and attempts correction."
