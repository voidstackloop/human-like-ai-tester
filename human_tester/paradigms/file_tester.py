"""File & Data Ingestion Pipeline Tester - Human File Quirks."""

import csv
import io
from typing import Dict, List, Optional
from ..personas import Persona
from ..reporter import AuditReporter


class FileTester:
    """Generates realistic human-created files with messy real-world quirks for ingestion testing."""

    def __init__(self, persona: Persona, reporter: Optional[AuditReporter] = None):
        self.persona = persona
        self.reporter = reporter or AuditReporter("File Ingestion Pipeline", persona.name)

    def generate_human_csv(self, include_bom: bool = True, mixed_delimiters: bool = False) -> str:
        """Generate a CSV exhibiting typical human export errors (Excel BOM, spaces, unescaped commas)."""
        lines = []

        # Row 1: Header with leading/trailing spaces
        lines.append(" Name , Email, Phone , Amount , Joined Date ")

        # Row 2: Standard row
        lines.append('Alice Smith, alice@example.com, (555) 123-4567, "$1,500.00", 2026-01-15')

        # Row 3: Name with comma not properly quoted, or trailing blank spaces
        lines.append('Bob Jones, Jr., bob@yahoo.com , 555-987-6543, 2500, 05/12/2026')

        # Row 4: Semicolon delimiter if European Excel saved it
        if mixed_delimiters:
            lines.append('Carlos Gomez;carlos@gmail.com;+34 612 345 678;3.200,50 €;12-05-2026')
        else:
            lines.append('Carlos Gomez, carlos@gmail.com, 555.333.2222, 3200.50, 12/05/2026')

        # Row 5: Accented name and trailing spaces
        lines.append('Renée O\'Connor, renee@gmai.com, 5554445555, "$ 450", 2026/03/01')

        # Row 6 & 7: Trailing blank rows (classic human copy-paste artifact)
        lines.append("")
        lines.append("   ")

        csv_content = "\n".join(lines)
        if include_bom:
            # Excel UTF-8 Byte Order Mark
            return "\ufeff" + csv_content
        return csv_content

    def generate_human_json(self) -> str:
        """Generate human-edited JSON with trailing commas or unquoted keys (human config error)."""
        # Note: Valid JSON cannot have trailing commas, but human-edited configs often do!
        return """{
  "project_name": "Antigravity Project",
  "enable_feature": true,
  "retry_count": "3",  // human entered string instead of int
  "allowed_users": [
    "alice@example.com",
    "bob@example.com",
  ], // Trailing comma from human manual editing
  "notes": "Added by admin on Friday afternoon"
}"""

    # -- Enriched file vectors ------------------------------------------------

    def generate_human_tsv(self) -> str:
        """Tab-delimited export with header spacing quirks (copy-paste from Excel)."""
        lines = [
            "Name\t Email \tPhone\t Amount ",
            "Alice Smith\talice@example.com\t(555) 123-4567\t$1,500.00",
            "Bob Jones\t bob@yahoo.com \t555-987-6543\t2500",
            "",
        ]
        return "\n".join(lines)

    def generate_header_case_variants(self) -> List[str]:
        """Same header row in different cases — pipelines must not be case-brittle."""
        return [
            "Name,Email,Phone,Amount",
            "NAME,EMAIL,PHONE,AMOUNT",
            "name,email,phone,amount",
            " Name , email,PHONE, Amount ",
        ]

    def validate_csv_robustness(self, csv_text: str) -> Dict:
        """Audit real CSV text for classic human traps; log one finding per trap.

        Traps: UTF-8 BOM, header spacing, blank/trailing rows, mixed ';'
        delimiters, rows with more naive-comma fields than the header
        (unescaped commas), and inconsistent column counts.
        """
        traps: List[Dict[str, str]] = []
        text = csv_text or ""
        lines = text.split("\n")

        if text.startswith("\ufeff"):
            traps.append({"id": "bom", "detail": "UTF-8 BOM present (\\ufeff) — naive parsers keep it in the first header."})
        header = lines[0].lstrip("\ufeff") if lines else ""
        if header != header.strip() or " ," in header or ", " in header and header.strip() != ",".join(
            c.strip() for c in header.split(",")
        ):
            traps.append({"id": "header_spacing", "detail": f"Header has stray spaces: {header!r}"})
        blank_rows = [i + 1 for i, l in enumerate(lines) if not l.strip()]
        if blank_rows:
            traps.append({"id": "blank_rows", "detail": f"Blank rows at line(s): {blank_rows}"})
        semicolon_rows = [i + 1 for i, l in enumerate(lines) if ";" in l]
        if semicolon_rows:
            traps.append({"id": "mixed_delimiters", "detail": f"Semicolons (EU-Excel style) at line(s): {semicolon_rows}"})

        # Proper parse: rows with more/fewer fields than the header reveal
        # unescaped commas (extra fields) or truncated rows (missing fields).
        try:
            parsed = list(csv.reader(io.StringIO(text.lstrip("\ufeff"))))
        except csv.Error:
            parsed = []
        if parsed:
            expected = len(parsed[0])
            for i, row in enumerate(parsed[1:], 2):
                if not any(c.strip() for c in row):
                    continue  # already covered by blank_rows
                if len(row) != expected:
                    traps.append({"id": "column_mismatch",
                                  "detail": f"Line {i} has {len(row)} fields, header has {expected} (unescaped comma?): {lines[i-1][:60]!r}"})
                    break

        for t in traps:
            self.reporter.add_finding(
                severity="MODERATE",
                category="File Ingestion",
                title=f"CSV trap present: {t['id']}",
                description="Real human exports carry this artifact; strict parsers choke on it.",
                simulated_action="Ingested human-authored CSV",
                system_reaction=t["detail"],
                recommendation="Strip BOM, trim headers, skip blank rows, sniff delimiters, use a tolerant CSV parser.",
            )
        return {"traps": traps, "trap_count": len(traps)}
