"""API & Backend Service Tester - Human Integration Mistakes."""

import json
import urllib.request
import urllib.error
from typing import Dict, List, Optional, Any
from ..personas import Persona
from ..reporter import AuditReporter


class APITester:
    """Simulates real human developers and API consumers making realistic integration mistakes."""

    def __init__(self, base_url: str, persona: Persona, reporter: Optional[AuditReporter] = None):
        self.base_url = base_url.rstrip("/")
        self.persona = persona
        self.reporter = reporter or AuditReporter(self.base_url, persona.name)

    def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        data: Optional[bytes] = None,
        timeout: float = 5.0,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("User-Agent", f"Human-AI-Tester/{self.persona.id}")
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)

        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return {
                    "status": resp.status,
                    "headers": dict(resp.headers),
                    "body": body,
                    "error": None,
                }
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            return {
                "status": e.code,
                "headers": dict(e.headers),
                "body": body,
                "error": f"HTTP {e.code}",
            }
        except Exception as e:
            return {"status": 0, "headers": {}, "body": "", "error": str(e)}

    def test_string_instead_of_number(self, endpoint: str, field_name: str, numeric_val: int = 42) -> Dict:
        """Humans frequently send numbers as strings e.g. {"count": "42"} instead of {"count": 42}."""
        payload_loose = json.dumps({field_name: str(numeric_val)}).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        res = self._make_request(endpoint, method="POST", headers=headers, data=payload_loose)

        # Check if API returns a clean 400 with helpful message or an unhandled 500 crash
        if res["status"] >= 500:
            self.reporter.add_finding(
                severity="CRITICAL",
                category="API Robustness",
                title=f"Server Crashed (500) on String Numeric Field '{field_name}'",
                description="Sending '\"42\"' instead of 42 caused an internal server crash rather than graceful type coercion or a 400 client error.",
                simulated_action=f"POST {endpoint} with {{'{field_name}': '{numeric_val}'}}",
                system_reaction=f"HTTP {res['status']}: {res['body'][:120]}",
                recommendation="Parse strings to numeric types gracefully in deserializers, or return 400 Bad Request.",
            )
        return res

    def test_missing_bearer_prefix(self, endpoint: str, raw_token: str = "token12345") -> Dict:
        """Humans often provide 'Authorization: <token>' instead of 'Bearer <token>'."""
        headers = {"Authorization": raw_token}
        res = self._make_request(endpoint, method="GET", headers=headers)

        if res["status"] >= 500:
            self.reporter.add_finding(
                severity="CRITICAL",
                category="API Security & Auth",
                title="Internal Server Error on Missing 'Bearer' Prefix",
                description="Header 'Authorization: token123' caused a crash instead of a 401 Unauthorized.",
                simulated_action="Authorization header without Bearer prefix",
                system_reaction=f"HTTP {res['status']}",
                recommendation="Handle missing auth schema gracefully with 401 and WWW-Authenticate header.",
            )
        return res

    def test_trailing_slashes(self, endpoint: str) -> Dict[str, Any]:
        """Humans are inconsistent with trailing slashes (/items vs /items/)."""
        ep_no_slash = endpoint.rstrip("/")
        ep_with_slash = endpoint.rstrip("/") + "/"

        res1 = self._make_request(ep_no_slash)
        res2 = self._make_request(ep_with_slash)

        status_diff = res1["status"] != res2["status"]
        if status_diff and (res1["status"] == 404 or res2["status"] == 404):
            self.reporter.add_finding(
                severity="FRICTION",
                category="API Discoverability",
                title="Trailing Slash Routing Inconsistency",
                description=f"Endpoint '{ep_no_slash}' returned {res1['status']} while '{ep_with_slash}' returned {res2['status']}.",
                simulated_action="Requested endpoint with and without trailing slash",
                system_reaction=f"{res1['status']} vs {res2['status']}",
                recommendation="Enable strict_slashes=False or auto-redirect trailing slashes to improve DX.",
            )
        return {"no_slash": res1["status"], "with_slash": res2["status"]}

    def test_unexpected_payload_fields(self, endpoint: str, standard_payload: Dict[str, Any]) -> Dict:
        """Humans often send extra deprecated or custom metadata fields."""
        dirty_payload = dict(standard_payload)
        dirty_payload["_notes"] = "entered by human"
        dirty_payload["custom_tag"] = 123

        payload_bytes = json.dumps(dirty_payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        res = self._make_request(endpoint, method="POST", headers=headers, data=payload_bytes)

        if res["status"] >= 500:
            self.reporter.add_finding(
                severity="CRITICAL",
                category="API Resilience",
                title="Unhandled Crash on Extra JSON Fields",
                description="Sending unexpected additional fields in payload caused a 500 server crash.",
                simulated_action=f"POST {endpoint} with unexpected properties",
                system_reaction=f"HTTP {res['status']}",
                recommendation="Configure schema validator to ignore or strip extra fields unless strict validation is required.",
            )
        return res
