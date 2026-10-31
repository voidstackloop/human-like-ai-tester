"""CLI & Terminal Application Tester - Human Simulation."""

import subprocess
import time
import random
from typing import Dict, List, Optional
from ..personas import Persona
from ..typo_engine import TypoEngine
from ..reporter import AuditReporter


class CLITester:
    """Simulates real human users operating terminal and CLI commands."""

    def __init__(self, command_base: List[str], persona: Persona, reporter: Optional[AuditReporter] = None):
        self.command_base = command_base
        self.persona = persona
        self.typo_engine = TypoEngine()
        self.reporter = reporter or AuditReporter(" ".join(command_base), persona.name)

    def test_help_and_discoverability(self) -> Dict:
        """Humans immediately type --help, -h, or 'help' when lost."""
        variants = [["--help"], ["-h"], ["help"], ["-?"]]
        results = {}
        for var in variants:
            cmd = self.command_base + var
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                success = proc.returncode == 0
                results[" ".join(var)] = {
                    "returncode": proc.returncode,
                    "stdout_len": len(proc.stdout),
                    "stderr_len": len(proc.stderr),
                }
            except Exception as e:
                results[" ".join(var)] = {"error": str(e)}

        # Evaluate human discoverability
        if all(r.get("returncode") != 0 for r in results.values()):
            self.reporter.add_finding(
                severity="FRICTION",
                category="CLI Usability",
                title="No Standard Help Flag Recognized",
                description="User could not find help using --help, -h, or help command.",
                simulated_action=f"{' '.join(self.command_base)} --help",
                system_reaction="Non-zero exit code or missing help message",
                recommendation="Implement standard -h and --help flags with concise usage examples.",
            )
        return results

    def test_flag_typos(self, valid_flags: List[str]) -> List[Dict]:
        """Humans frequently make minor typos in CLI flags (--verboose, --hlpe)."""
        scenarios = []
        for flag in valid_flags:
            # Generate a realistic typo in the flag
            clean = flag.lstrip("-")
            prefix = "--" if flag.startswith("--") else "-"
            typo_flag = prefix + self.typo_engine.introduce_typos(clean, error_rate=0.35)
            if typo_flag == flag:
                typo_flag = prefix + self.typo_engine.introduce_fat_finger(clean)

            cmd = self.command_base + [typo_flag]
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                output = (proc.stderr or proc.stdout).lower()
                # Check if CLI suggests the correct flag ("Did you mean --verbose?")
                has_suggestion = "did you mean" in output or clean in output

                scenario = {
                    "original_flag": flag,
                    "typo_flag": typo_flag,
                    "returncode": proc.returncode,
                    "has_suggestion": has_suggestion,
                    "output_preview": (proc.stderr or proc.stdout)[:200],
                }
                scenarios.append(scenario)

                if not has_suggestion and proc.returncode != 0:
                    self.reporter.add_finding(
                        severity="MODERATE",
                        category="CLI Error Guidance",
                        title=f"Unhelpful Typo Error on '{typo_flag}'",
                        description=f"When human typed typo flag '{typo_flag}', the tool did not suggest the intended '{flag}'.",
                        simulated_action=f"{' '.join(cmd)}",
                        system_reaction=(proc.stderr or proc.stdout).strip()[:100] or f"Exit {proc.returncode}",
                        recommendation=f"Add fuzzy matching / 'Did you mean {flag}?' suggestions for mistyped options.",
                    )
            except Exception as e:
                scenarios.append({"typo_flag": typo_flag, "error": str(e)})

        return scenarios

    def test_unquoted_spaces_in_path(self, arg_flag: Optional[str] = None) -> Dict:
        """Humans often forget quotes when passing paths with spaces ('my project/data.txt')."""
        unquoted = ["my", "project", "folder/test data.txt"]
        cmd = list(self.command_base)
        if arg_flag:
            cmd.append(arg_flag)
        cmd.extend(unquoted)

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            out = (proc.stderr or proc.stdout).lower()
            return {
                "cmd": cmd,
                "returncode": proc.returncode,
                "output": (proc.stderr or proc.stdout)[:300],
            }
        except Exception as e:
            return {"error": str(e)}

    def test_interactive_prompts(self, natural_responses: List[str]) -> List[Dict]:
        """Humans type 'yeah', 'yep', 'nope' or just hit enter on interactive prompts."""
        # Test vectors: empty Enter, natural answers, raw invalid types
        results = []
        for resp in natural_responses:
            try:
                proc = subprocess.run(
                    self.command_base,
                    input=resp + "\n",
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                results.append({
                    "input": resp,
                    "returncode": proc.returncode,
                    "output": proc.stdout[:200],
                })
            except Exception as e:
                results.append({"input": resp, "error": str(e)})
        return results
