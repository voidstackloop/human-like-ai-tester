"""CLI & Terminal Application Tester - Human Simulation."""

import subprocess
import time
import signal
from typing import Dict, List, Optional
from ..personas import Persona
from ..typo_engine import TypoEngine
from ..reporter import AuditReporter

# What humans actually type at interactive prompts.
COLLOQUIAL_PROMPT_ANSWERS: List[str] = ["", "yeah", "yep", "nah", "nope", "sure", "n/a", " "]
CTRL_C_EXIT_CODES = {130, -signal.SIGINT, 2, 1}


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

    # -- Enriched CLI vectors -------------------------------------------------

    def test_empty_enter_and_colloquial(self) -> List[Dict]:
        """Press bare Enter plus colloquial answers; record crashes vs reprompts."""
        results = self.test_interactive_prompts(COLLOQUIAL_PROMPT_ANSWERS)
        for r in results:
            out = (r.get("output") or "").lower()
            if "traceback" in out and r.get("returncode") not in (None, 0):
                self.reporter.add_finding(
                    severity="FRICTION",
                    category="CLI Robustness",
                    title=f"Interactive prompt crashed on {r['input']!r}",
                    description="Bare Enter / colloquial answer dumped a traceback instead of reprompting.",
                    simulated_action=f"Answered prompt with {r['input']!r}",
                    system_reaction=r.get("output", "")[:120],
                    recommendation="Validate prompt input; reprompt with an example instead of crashing.",
                )
        return results

    def test_ctrl_c_during_long_run(self, wait_before_sigint: float = 1.0) -> Dict:
        """Start the command, send SIGINT like an impatient human, check cleanup.

        Flags raw tracebacks (unhandled KeyboardInterrupt); graceful 130-style
        exits pass silently.
        """
        try:
            proc = subprocess.Popen(
                self.command_base, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
        except Exception as e:
            return {"error": str(e)}

        try:
            time.sleep(wait_before_sigint)
            if proc.poll() is not None:
                out, err = proc.communicate()
                return {"exited_early": True, "returncode": proc.returncode,
                        "output": (out or err or "")[:200]}
            proc.send_signal(signal.SIGINT)
            try:
                out, err = proc.communicate(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
                out, err = proc.communicate()
                self.reporter.add_finding(
                    severity="FRICTION",
                    category="CLI Robustness",
                    title="Command ignored Ctrl-C and had to be killed",
                    description="SIGINT did nothing; the human had to close the terminal.",
                    simulated_action=f"Pressed Ctrl-C on {' '.join(self.command_base)}",
                    system_reaction="Still running after 3s; SIGKILL required",
                    recommendation="Handle SIGINT: stop promptly, clean up partial state, exit 130.",
                )
                return {"ignored_sigint": True}
            combined = ((out or "") + (err or "")).lower()
            if "traceback" in combined:
                self.reporter.add_finding(
                    severity="MODERATE",
                    category="CLI Robustness",
                    title="Ctrl-C dumped a raw traceback",
                    description="KeyboardInterrupt escaped to the user instead of a clean abort line.",
                    simulated_action=f"Pressed Ctrl-C on {' '.join(self.command_base)}",
                    system_reaction=(out or err or "")[:150],
                    recommendation="Catch KeyboardInterrupt; print 'Aborted.' and exit 130.",
                )
            return {"returncode": proc.returncode, "graceful": proc.returncode in CTRL_C_EXIT_CODES,
                    "output": ((out or err) or "")[:200]}
        finally:
            if proc.poll() is None:
                proc.kill()

    def test_extra_whitespace_and_empty_args(self) -> Dict:
        """Pass empty-string args and stray dashes the way paste accidents do."""
        cmd = list(self.command_base) + ["", "--", " "]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            out = (proc.stderr or proc.stdout)
            if "traceback" in out.lower():
                self.reporter.add_finding(
                    severity="MODERATE",
                    category="CLI Robustness",
                    title="Empty/paste-artifact args caused a traceback",
                    description="Stray empty args from a bad paste crashed instead of a usage error.",
                    simulated_action=f"{' '.join(self.command_base)} '' -- ' '",
                    system_reaction=out[:150],
                    recommendation="Filter empty args; treat bare '--' as end-of-options per convention.",
                )
            return {"returncode": proc.returncode, "output": out[:300]}
        except Exception as e:
            return {"error": str(e)}
