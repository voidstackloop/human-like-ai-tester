"""Desktop GUI Application Tester - Human Simulation (heuristic, stdlib-only).

No GUI driver is required: the tester audits supplied layout metadata
(button spacing, breakpoints, dialog behavior) and emits findings plus a
manual walkthrough script a human or agent can execute against the real app.
"""

from typing import Dict, List, Optional
from ..personas import Persona
from ..cognitive_engine import CognitiveEngine
from ..reporter import AuditReporter


class DesktopTester:
    """Simulates real human users operating desktop GUI applications."""

    def __init__(self, app_name: str, persona: Persona, reporter: Optional[AuditReporter] = None):
        self.app_name = app_name
        self.persona = persona
        self.cognitive = CognitiveEngine(persona)
        self.reporter = reporter or AuditReporter(app_name, persona.name)

    def audit_button_proximity(
        self, submit_label: str = "Submit", cancel_label: str = "Cancel", distance_px: float = 100.0
    ) -> Dict:
        """Flag Cancel/Submit pairs close enough for fatigued misclicks (<40px)."""
        risky = distance_px < 40.0
        if risky:
            self.reporter.add_finding(
                severity="FRICTION",
                category="Desktop Layout",
                title=f"'{cancel_label}' sits {distance_px:.0f}px from '{submit_label}' — misclick risk",
                description=f"{self.persona.name} can torpedo a completed form with one slip.",
                simulated_action=f"Aimed for '{submit_label}', adjacent '{cancel_label}' within slip range",
                system_reaction=f"Buttons {distance_px:.0f}px apart with similar emphasis",
                recommendation="Separate destructive actions by 40px+, de-emphasize Cancel, confirm destructive clicks.",
            )
            self.cognitive.record_event("PROXIMITY_RISK", "Cancel/Submit too close", penalty=8.0)
        return {"distance_px": distance_px, "risky": risky}

    def simulate_window_resize(self, breakpoints: List[int], clipped_at: Optional[List[int]] = None) -> Dict:
        """Check supplied window widths for clipped actions (heuristic).

        Args:
            breakpoints: widths the layout claims to support, e.g. [1280, 1024, 800].
            clipped_at: widths where the primary action is clipped (from manual check).
        """
        clipped_at = clipped_at or []
        results = {}
        for width in breakpoints:
            clipped = width in clipped_at
            results[width] = {"clipped": clipped}
            if clipped:
                self.reporter.add_finding(
                    severity="FRICTION",
                    category="Desktop Layout",
                    title=f"Primary action clipped at {width}px window width",
                    description="Resizing mid-flow hides the submit path with no scroll cue.",
                    simulated_action=f"Resized window to {width}px mid-task",
                    system_reaction="Submit button clipped / unreachable",
                    recommendation="Responsive layout with min sizes and scrollable content regions.",
                )
                self.cognitive.record_event("RESIZE_CLIP", f"Clipped at {width}px", penalty=10.0)
        return results

    def simulate_dialog_cancel_midway(self, dialog_name: str, leaves_half_state: bool) -> Dict:
        """Verify cancelling a file/settings dialog is an atomic no-op."""
        if leaves_half_state:
            self.reporter.add_finding(
                severity="CRITICAL",
                category="Desktop State",
                title=f"Cancelling '{dialog_name}' leaves a half-applied state",
                description="User cancelled but the app kept partial changes with no undo.",
                simulated_action=f"Opened '{dialog_name}', changed values, pressed Cancel",
                system_reaction="Partial state persisted; no undo offered",
                recommendation="Treat dialog Cancel as atomic no-op; confirm-or-revert partial edits.",
            )
            self.cognitive.record_event("DIALOG_HALF_STATE", dialog_name, penalty=30.0)
        return {"dialog": dialog_name, "atomic_cancel": not leaves_half_state}

    def simulate_shortcut_misuse(self, shortcut: str, collides_with_os: bool) -> Dict:
        """Check an app shortcut against OS/browser defaults (heuristic)."""
        if collides_with_os:
            self.reporter.add_finding(
                severity="MODERATE",
                category="Desktop Shortcuts",
                title=f"Shortcut {shortcut} collides with OS/browser default",
                description="Muscle-memory shortcut fires the wrong action; user loses work.",
                simulated_action=f"Pressed {shortcut} expecting app action",
                system_reaction="OS/browser default fired instead",
                recommendation="Scope shortcuts to the app window; confirm before destructive defaults.",
            )
        return {"shortcut": shortcut, "collision": collides_with_os}

    def simulate_drag_drop_miss(self, target_size_px: float, missed: bool) -> Dict:
        """Verify missed drops fail loudly instead of silently doing nothing."""
        if missed:
            severity = "FRICTION" if target_size_px < 64 else "MODERATE"
            self.reporter.add_finding(
                severity=severity,
                category="Desktop Drag-Drop",
                title=f"Drop target ({target_size_px:.0f}px) missed with no feedback",
                description="File landed outside a small target; import silently did nothing.",
                simulated_action="Dragged file onto drop zone, missed by a few px",
                system_reaction="No highlight, no error, no import",
                recommendation="Large drop zone with hover highlight + explicit error on missed drop.",
            )
        return {"target_size_px": target_size_px, "missed": missed}

    def generate_manual_script(self) -> List[str]:
        """Human-executable desktop walkthrough for this persona."""
        return [
            f"1. As {self.persona.name}: tab through the main window using keyboard only — is focus always visible?",
            "2. Complete the primary form, then aim for Submit: is Cancel far enough away to avoid slips?",
            "3. Resize the window to 1024px then 800px mid-flow: does the primary action stay reachable?",
            "4. Open the file/settings dialog, change two values, press Cancel: is NOTHING applied?",
            "5. Press the app's top 3 shortcuts: does any fire an OS/browser default instead?",
            "6. Drag a file just outside the drop zone: do you get a clear error (not silence)?",
            "7. If any step stalls >2s with no feedback, click rapidly: is the action idempotent?",
        ]
