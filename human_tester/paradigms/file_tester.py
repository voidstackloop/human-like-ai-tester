"""File & Data Ingestion Pipeline Tester - Human File Quirks."""

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
