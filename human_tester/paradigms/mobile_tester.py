"""Mobile & Touch Application Tester - Human Simulation (heuristic, stdlib-only).

Audits supplied mobile-layout metadata (action placement, keyboard overlap,
rotation behavior, deep links, permission rationale) and emits findings plus
a manual walkthrough script for the real device.
"""

from typing import Dict, List, Optional
from ..personas import Persona
from ..cognitive_engine import CognitiveEngine
from ..reporter import AuditReporter

THUMB_SAFE_ZONES = {"bottom-center", "bottom-right", "bottom-left", "center"}
THUMB_DEAD_ZONES = {"top-right", "top-left", "top-center"}


class MobileTester:
    """Simulates real human users on phones and tablets."""

    def __init__(self, app_name: str, persona: Persona, reporter: Optional[AuditReporter] = None):
        self.app_name = app_name
        self.persona = persona
        self.cognitive = CognitiveEngine(persona)
        self.reporter = reporter or AuditReporter(app_name, persona.name)

    def audit_thumb_reach(self, primary_action_position: str) -> Dict:
        """Flag primary actions placed outside the one-handed thumb zone."""
        pos = primary_action_position.strip().lower()
        unreachable = pos in THUMB_DEAD_ZONES
        if unreachable:
            self.reporter.add_finding(
                severity="FRICTION",
                category="Mobile Ergonomics",
                title=f"Primary action in thumb dead zone ({pos})",
                description=f"{self.persona.name} one-hands the phone; top-corner actions invite drops and mis-taps.",
                simulated_action="Reached for primary action one-handed",
                system_reaction=f"Action placed at {pos}, outside thumb zone",
                recommendation="Move primary actions to bottom half / thumb zone; keep destructive ones away.",
            )
            self.cognitive.record_event("THUMB_REACH", pos, penalty=8.0)
        return {"position": pos, "unreachable_one_handed": unreachable}

    def audit_keyboard_overlap(self, submit_visible_with_keyboard: bool) -> Dict:
        """Verify the soft keyboard does not cover submit/errors."""
        if not submit_visible_with_keyboard:
            self.reporter.add_finding(
                severity="CRITICAL",
                category="Mobile Layout",
                title="Soft keyboard covers submit button and inline errors",
                description="User types blind, cannot see errors, and assumes the app is broken.",
                simulated_action="Focused a field with the keyboard open",
                system_reaction="Submit + errors hidden behind keyboard",
                recommendation="Scroll focused field and submit above the keyboard (visualViewport); keep errors visible.",
            )
            self.cognitive.record_event("KEYBOARD_OVERLAP", "submit covered", penalty=25.0)
        return {"submit_visible": submit_visible_with_keyboard}

    def test_orientation_flip(self, state_preserved: bool) -> Dict:
        """Verify rotation does not wipe typed data or restart the flow."""
        if not state_preserved:
            self.reporter.add_finding(
                severity="CRITICAL",
                category="Mobile State",
                title="Orientation flip wipes form state",
                description="Rotating the phone destroyed everything the user typed.",
                simulated_action="Rotated phone mid-form",
                system_reaction="Form reset / flow restarted",
                recommendation="Persist form state across configuration changes; restore focus after rotation.",
            )
            self.cognitive.record_event("ROTATION_WIPE", "state lost", penalty=35.0)
        return {"state_preserved": state_preserved}

    def test_deep_link(self, url: str, cold_start_ok: bool, preserves_context: bool) -> Dict:
        """Verify deep links land in context on cold start (heuristic inputs)."""
        if not (cold_start_ok and preserves_context):
            self.reporter.add_finding(
                severity="FRICTION",
                category="Mobile Navigation",
                title=f"Deep link drops context: {url}",
                description="Shared link opened the app but not the content; user must re-navigate.",
                simulated_action=f"Tapped shared link {url} with app closed",
                system_reaction=f"cold_start_ok={cold_start_ok}, context_ok={preserves_context}",
                recommendation="Resolve deep links to content on cold start; show a loading skeleton, not home.",
            )
        return {"url": url, "cold_start_ok": cold_start_ok, "preserves_context": preserves_context}

    def audit_permission_dialog(self, permission: str, rationale_shown: bool, graceful_denial: bool) -> Dict:
        """Verify permission prompts explain why and survive denial."""
        if not rationale_shown or not graceful_denial:
            self.reporter.add_finding(
                severity="FRICTION",
                category="Mobile Permissions",
                title=f"'{permission}' prompt lacks rationale or hard-crashes on deny",
                description="User denies a scary unexplained prompt and the flow dead-ends.",
                simulated_action=f"Denied '{permission}' at prompt",
                system_reaction=f"rationale={rationale_shown}, graceful={graceful_denial}",
                recommendation="Pre-prompt with a plain-language why; keep the flow usable after denial.",
            )
        return {"permission": permission, "rationale": rationale_shown, "graceful": graceful_denial}

    def simulate_rage_tap(self, response_time_seconds: float) -> Dict:
        """Reuse the cognitive rage model for sluggish touch targets."""
        did_rage, count, intervals = self.cognitive.trigger_rage_click_check(response_time_seconds)
        self.reporter.sync_frustration(self.cognitive.frustration_score)
        if did_rage:
            self.reporter.metrics["rage_clicks_attempted"] += 1
        return {"did_rage_tap": did_rage, "tap_count": count, "intervals_ms": intervals}

    def generate_manual_script(self) -> List[str]:
        """Human-executable mobile walkthrough for this persona."""
        return [
            f"1. As {self.persona.name}: one-hand the phone — can your thumb reach the primary action?",
            "2. Focus each field: does the keyboard ever cover submit or error text?",
            "3. Type half a form, rotate the phone: is EVERYTHING preserved?",
            "4. Cold-start the app from a shared deep link: do you land on the content?",
            "5. Deny each permission prompt: does the flow stay usable with a clear why?",
            "6. On the slowest button, tap 4x fast: exactly one request must fire.",
        ]
