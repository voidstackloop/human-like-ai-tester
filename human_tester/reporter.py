"""Human-Centric Usability & Robustness Audit Report Generator."""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time


@dataclass
class Finding:
    severity: str        # 'CRITICAL', 'FRICTION', 'MODERATE', 'DELIGHT'
    category: str        # 'Error Recovery', 'Formatting', 'Latency/Impatience', 'Navigation', 'Visual Clarity'
    title: str
    description: str
    simulated_action: str
    system_reaction: str
    recommendation: str


class AuditReporter:
    """Compiles and formats human user test results into structured audit reports."""

    def __init__(self, target_name: str, persona_name: str):
        self.target_name = target_name
        self.persona_name = persona_name
        self.start_time = time.time()
        self.findings: List[Finding] = []
        self.frustration_score = 0.0
        self.metrics: Dict[str, any] = {
            "typos_tested": 0,
            "rage_clicks_attempted": 0,
            "format_quirks_tested": 0,
            "unhandled_errors": 0,
        }

    def add_finding(
        self,
        severity: str,
        category: str,
        title: str,
        description: str,
        simulated_action: str,
        system_reaction: str,
        recommendation: str,
    ):
        self.findings.append(
            Finding(
                severity=severity.upper(),
                category=category,
                title=title,
                description=description,
                simulated_action=simulated_action,
                system_reaction=system_reaction,
                recommendation=recommendation,
            )
        )

    def generate_markdown(self) -> str:
        """Render standard markdown report."""
        duration = round(time.time() - self.start_time, 2)
        verdict = "PASS"
        if any(f.severity == "CRITICAL" for f in self.findings):
            verdict = "CRITICAL USABILITY BLOCKERS"
        elif self.frustration_score >= 60.0 or any(f.severity == "FRICTION" for f in self.findings):
            verdict = "HIGH HUMAN FRICTION"
        else:
            verdict = "PASS - RESILIENT TO HUMAN ERROR"

        md = []
        md.append(f"# 🧑 Human-Centric Usability & Robustness Audit Report\n")
        md.append(f"## 1. Executive Summary")
        md.append(f"- **Target Application**: `{self.target_name}`")
        md.append(f"- **Tested Persona**: **{self.persona_name}**")
        md.append(f"- **Session Duration**: {duration}s")
        md.append(f"- **Frustration Index**: **{self.frustration_score:.1f}%**")
        md.append(f"- **Overall Verdict**: **{verdict}**\n")

        md.append(f"## 2. Test Execution Metrics")
        md.append(f"| Metric | Count |")
        md.append(f"| :--- | :--- |")
        for k, v in self.metrics.items():
            md.append(f"| {k.replace('_', ' ').title()} | {v} |")
        md.append("")

        md.append(f"## 3. Human Mistake & Friction Audit")
        if not self.findings:
            md.append("_No usability issues detected. Application handled human behavior gracefully._\n")
        else:
            md.append(f"| Severity | Category | Finding | Simulated Action | System Reaction |")
            md.append(f"| :--- | :--- | :--- | :--- | :--- |")
            for f in self.findings:
                icon = "🔴" if f.severity == "CRITICAL" else ("🟡" if f.severity == "FRICTION" else ("🔵" if f.severity == "MODERATE" else "🟢"))
                md.append(f"| {icon} {f.severity} | {f.category} | {f.title} | `{f.simulated_action}` | {f.system_reaction} |")
            md.append("")

            md.append(f"## 4. Detailed Findings & Developer Action Plan\n")
            for idx, f in enumerate(self.findings, 1):
                md.append(f"### {idx}. [{f.severity}] {f.title}")
                md.append(f"- **Category**: {f.category}")
                md.append(f"- **What the Human Did**: {f.simulated_action}")
                md.append(f"- **What Happened**: {f.system_reaction}")
                md.append(f"- **Human Impact**: {f.description}")
                md.append(f"- **Recommended Fix**: {f.recommendation}\n")

        return "\n".join(md)

    def to_json(self) -> str:
        """Export as structured JSON."""
        return json.dumps(
            {
                "target": self.target_name,
                "persona": self.persona_name,
                "frustration_score": self.frustration_score,
                "metrics": self.metrics,
                "findings": [f.__dict__ for f in self.findings],
            },
            indent=2,
        )
