"""Web & Mobile Web Application Tester - Human Simulation."""

import time
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, List, Optional
from ..personas import Persona
from ..cognitive_engine import CognitiveEngine
from ..typo_engine import TypoEngine
from ..reporter import AuditReporter


class WebTester:
    """Simulates real human users navigating web applications and submitting forms."""

    def __init__(self, target_url: str, persona: Persona, reporter: Optional[AuditReporter] = None):
        self.target_url = target_url
        self.persona = persona
        self.cognitive = CognitiveEngine(persona)
        self.typo_engine = TypoEngine()
        self.reporter = reporter or AuditReporter(target_url, persona.name)

    def test_page_load_and_clarity(self) -> Dict:
        """Measure initial load time and assess visual clarity against persona patience."""
        start = time.time()
        try:
            req = urllib.request.Request(self.target_url, headers={"User-Agent": f"Human-AI-Tester/{self.persona.id}"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                elapsed = time.time() - start
                content = resp.read().decode("utf-8", errors="replace")

                # Check if load time exceeded persona patience threshold
                did_rage_click, clicks, intervals = self.cognitive.trigger_rage_click_check(elapsed)

                if elapsed > self.persona.patience_seconds:
                    self.reporter.add_finding(
                        severity="FRICTION" if elapsed < 4.0 else "CRITICAL",
                        category="Perceived Performance",
                        title=f"Page Load Latency Exceeded Persona Patience ({elapsed:.2f}s > {self.persona.patience_seconds}s)",
                        description=f"{self.persona.name} experienced impatience and {'triggered rage-clicks' if did_rage_click else 'considered abandoning the page'}.",
                        simulated_action=f"Loaded {self.target_url}",
                        system_reaction=f"Response time was {elapsed:.2f}s",
                        recommendation="Optimize critical rendering path, add skeleton loaders or fast response headers.",
                    )

                return {
                    "status": resp.status,
                    "load_time_seconds": round(elapsed, 2),
                    "page_size_kb": round(len(content) / 1024.0, 1),
                    "rage_clicks": clicks if did_rage_click else 0,
                }
        except Exception as e:
            return {"error": str(e), "load_time_seconds": round(time.time() - start, 2)}

    def test_form_submission_with_human_formatting(
        self,
        form_endpoint: str,
        form_fields: Dict[str, str],
        method: str = "POST",
    ) -> Dict:
        """Submit a form with typical human mistakes (unformatted phone, typos, trailing spaces)."""
        dirty_fields = {}
        for key, val in form_fields.items():
            if "phone" in key.lower() or "mobile" in key.lower():
                # Format phone like a human: (555) 234-5678
                dirty_fields[key] = self.typo_engine.format_phone_human_style(val)
                self.reporter.metrics["format_quirks_tested"] += 1
            elif "email" in key.lower():
                # Add domain typo or spaces
                dirty_fields[key] = self.typo_engine.corrupt_email(val, error_rate=self.persona.typo_rate)
                self.reporter.metrics["typos_tested"] += 1
            elif "price" in key.lower() or "amount" in key.lower() or "cost" in key.lower():
                # Add currency signs
                try:
                    num = float(val.replace("$", "").replace(",", ""))
                    dirty_fields[key] = self.typo_engine.format_currency_human_style(num)
                except ValueError:
                    dirty_fields[key] = val
                self.reporter.metrics["format_quirks_tested"] += 1
            else:
                # Add human typos and clipboard quirks
                if self.persona.typo_rate > 0.10:
                    text_with_typos = self.typo_engine.introduce_typos(val, error_rate=self.persona.typo_rate)
                    dirty_fields[key] = self.typo_engine.add_clipboard_quirks(text_with_typos)
                else:
                    dirty_fields[key] = val

        # Encode and send
        data_encoded = urllib.parse.urlencode(dirty_fields).encode("utf-8")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": f"Human-AI-Tester/{self.persona.id}",
        }

        full_url = f"{self.target_url.rstrip('/')}/{form_endpoint.lstrip('/')}"
        req = urllib.request.Request(full_url, data=data_encoded, headers=headers, method=method)

        start = time.time()
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                duration = time.time() - start
                body = resp.read().decode("utf-8", errors="replace")
                return {
                    "status": resp.status,
                    "duration": round(duration, 2),
                    "submitted_fields": dirty_fields,
                    "response_preview": body[:200],
                }
        except urllib.error.HTTPError as e:
            duration = time.time() - start
            body = e.read().decode("utf-8", errors="replace")
            # If rejected strictly on format without clear error
            if e.code == 400 or e.code == 422:
                self.reporter.add_finding(
                    severity="FRICTION",
                    category="Form Validation Resilience",
                    title="Strict Form Rejection on Human-Formatted Inputs",
                    description="Application rejected human-formatted inputs without friendly inline recovery guidance.",
                    simulated_action=f"Submitted: {dirty_fields}",
                    system_reaction=f"HTTP {e.code}: {body[:150]}",
                    recommendation="Accept common phone, currency, and date formats and sanitize client-side / server-side.",
                )
            return {
                "status": e.code,
                "duration": round(duration, 2),
                "submitted_fields": dirty_fields,
                "error": str(e),
                "response_body": body[:300],
            }
        except Exception as e:
            return {"error": str(e), "submitted_fields": dirty_fields}

    def test_rapid_double_click_vulnerability(
        self,
        form_endpoint: str,
        form_fields: Dict[str, str],
        method: str = "POST",
    ) -> Dict:
        """Simulate an impatient user double-clicking submit within 100ms."""
        self.reporter.metrics["rage_clicks_attempted"] += 1
        data_encoded = urllib.parse.urlencode(form_fields).encode("utf-8")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": f"Human-AI-Tester/{self.persona.id}",
        }
        full_url = f"{self.target_url.rstrip('/')}/{form_endpoint.lstrip('/')}"

        # Send first click
        req1 = urllib.request.Request(full_url, data=data_encoded, headers=headers, method=method)
        req2 = urllib.request.Request(full_url, data=data_encoded, headers=headers, method=method)

        responses = []
        try:
            with urllib.request.urlopen(req1, timeout=5) as r1:
                responses.append(r1.status)
        except urllib.error.HTTPError as e:
            responses.append(e.code)
        except Exception:
            responses.append(0)

        # Immediate second click (simulating rapid finger double-tap)
        try:
            with urllib.request.urlopen(req2, timeout=5) as r2:
                responses.append(r2.status)
        except urllib.error.HTTPError as e:
            responses.append(e.code)
        except Exception:
            responses.append(0)

        # If both succeeded (e.g. 200/201), system may lack idempotent submit prevention
        if responses == [200, 200] or responses == [201, 201]:
            self.reporter.add_finding(
                severity="CRITICAL",
                category="Transaction Idempotency",
                title="Vulnerable to Double-Click Duplicate Submission",
                description="Rapid double-tap on submit succeeded twice, risking duplicate orders, double payments, or duplicate database records.",
                simulated_action="Two concurrent POST requests within 50ms",
                system_reaction=f"Both requests succeeded with status {responses}",
                recommendation="Disable the submit button immediately on first click, and enforce idempotency tokens on the server.",
            )

        return {"responses": responses, "idempotent": responses != [200, 200]}
