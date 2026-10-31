"""Human-Centric Usability & Robustness Audit Report Generator."""

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import time

SEVERITY_ORDER = {"CRITICAL": 0, "FRICTION": 1, "MODERATE": 2, "DELIGHT": 3}


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
        self.metrics: Dict[str, Any] = {
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

    def sync_frustration(self, score: float) -> float:
        """Adopt the highest-seen frustration score from a cognitive engine."""
        self.frustration_score = max(self.frustration_score, max(0.0, min(100.0, score)))
        return self.frustration_score

    def severity_counts(self) -> Dict[str, int]:
        """Count findings per severity level."""
        counts: Dict[str, int] = {"CRITICAL": 0, "FRICTION": 0, "MODERATE": 0, "DELIGHT": 0}
        for f in self.findings:
            counts[f.severity] = counts.get(f.severity, 0) + 1
        return counts

    def sorted_findings(self) -> List[Finding]:
        """Findings ordered CRITICAL first, DELIGHT last."""
        return sorted(self.findings, key=lambda f: SEVERITY_ORDER.get(f.severity, 9))

    def dedupe_findings(self) -> int:
        """Collapse identical (severity, category, title) findings from multi-persona
        sweeps into one entry suffixed with a hit count. Returns findings removed."""
        seen: Dict[tuple, Finding] = {}
        counts: Dict[tuple, int] = {}
        for f in self.findings:
            key = (f.severity, f.category, f.title)
            counts[key] = counts.get(key, 0) + 1
            if key not in seen:
                seen[key] = f
        merged: List[Finding] = []
        for key, finding in seen.items():
            if counts[key] > 1:
                finding.title = f"{finding.title} (×{counts[key]} personas)"
            merged.append(finding)
        removed = len(self.findings) - len(merged)
        self.findings = merged
        return removed

    def generate_remediation_plan(self, top_n: Optional[int] = None) -> str:
        """Prioritized developer fix list, most abandonment-risky first."""
        ordered = self.sorted_findings()
        if top_n is not None:
            ordered = ordered[: max(0, top_n)]
        if not ordered:
            return "No fixes required — the flow survived human behavior."
        lines = []
        for idx, f in enumerate(ordered, 1):
            icon = "🔴" if f.severity == "CRITICAL" else ("🟡" if f.severity == "FRICTION" else "🔵")
            lines.append(f"{idx}. {icon} **{f.title}** — {f.recommendation}")
        return "\n".join(lines)

    def verdict(self) -> str:
        """Overall session verdict string."""
        if any(f.severity == "CRITICAL" for f in self.findings):
            return "CRITICAL USABILITY BLOCKERS"
        elif self.frustration_score >= 60.0 or any(f.severity == "FRICTION" for f in self.findings):
            return "HIGH HUMAN FRICTION"
        return "PASS - RESILIENT TO HUMAN ERROR"

    def generate_markdown(self) -> str:
        """Render standard markdown report."""
        duration = round(time.time() - self.start_time, 2)
        verdict = self.verdict()

        md = []
        md.append("# 🧑 Human-Centric Usability & Robustness Audit Report\n")
        md.append("## 1. Executive Summary")
        md.append(f"- **Target Application**: `{self.target_name}`")
        md.append(f"- **Tested Persona**: **{self.persona_name}**")
        md.append(f"- **Session Duration**: {duration}s")
        md.append(f"- **Frustration Index**: **{self.frustration_score:.1f}%**")
        md.append(f"- **Overall Verdict**: **{verdict}**\n")

        md.append("## 2. Test Execution Metrics")
        md.append("| Metric | Count |")
        md.append("| :--- | :--- |")
        for k, v in self.metrics.items():
            md.append(f"| {k.replace('_', ' ').title()} | {v} |")
        counts = self.severity_counts()
        md.append(f"| Critical Findings | {counts.get('CRITICAL', 0)} |")
        md.append(f"| Friction Findings | {counts.get('FRICTION', 0)} |")
        md.append("")

        md.append("## 3. Human Mistake & Friction Audit")
        if not self.findings:
            md.append("_No usability issues detected. Application handled human behavior gracefully._\n")
        else:
            md.append("| Severity | Category | Finding | Simulated Action | System Reaction |")
            md.append("| :--- | :--- | :--- | :--- | :--- |")
            for f in self.sorted_findings():
                icon = "🔴" if f.severity == "CRITICAL" else ("🟡" if f.severity == "FRICTION" else ("🔵" if f.severity == "MODERATE" else "🟢"))
                md.append(f"| {icon} {f.severity} | {f.category} | {f.title} | `{f.simulated_action}` | {f.system_reaction} |")
            md.append("")

            md.append("## 4. Detailed Findings & Developer Action Plan\n")
            for idx, f in enumerate(self.sorted_findings(), 1):
                md.append(f"### {idx}. [{f.severity}] {f.title}")
                md.append(f"- **Category**: {f.category}")
                md.append(f"- **What the Human Did**: {f.simulated_action}")
                md.append(f"- **What Happened**: {f.system_reaction}")
                md.append(f"- **Human Impact**: {f.description}")
                md.append(f"- **Recommended Fix**: {f.recommendation}\n")

            md.append("## 5. Prioritized Remediation Plan\n")
            md.append(self.generate_remediation_plan())
            md.append("")

        return "\n".join(md)

    def to_json(self) -> str:
        """Export as structured JSON."""
        return json.dumps(
            {
                "target": self.target_name,
                "persona": self.persona_name,
                "frustration_score": self.frustration_score,
                "verdict": self.verdict(),
                "severity_counts": self.severity_counts(),
                "metrics": self.metrics,
                "findings": [f.__dict__ for f in self.sorted_findings()],
            },
            indent=2,
        )

    def save_markdown(self, path: str) -> str:
        """Write the markdown report to a file; returns the path."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.generate_markdown())
        return path

    def save_json(self, path: str) -> str:
        """Write the JSON report to a file; returns the path."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_json())
        return path
