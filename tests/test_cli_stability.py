"""Stability guards for the CLI contract and packaging hygiene.

Network-free: subprocess cases only invoke --version/--help paths, and
in-process cases never touch the network.
"""

import io
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import human_tester
from human_tester.cli import main

REPO_ROOT = Path(__file__).resolve().parent.parent

# Every subcommand that shipped in v0.2.0. Removing or renaming one is a
# breaking change and must fail loudly here first.
EXPECTED_SUBCOMMANDS = [
    "personas",
    "simulate",
    "test-cli",
    "test-web",
    "test-api",
    "test-chat",
    "test-desktop",
    "test-mobile",
    "validate-file",
    "audit",
    "generate-file",
    "demo",
]


def run_main(argv):
    """Run the CLI in-process, capturing output. Returns (exit_code, stdout, stderr)."""
    stdout, stderr = io.StringIO(), io.StringIO()
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            main(argv)
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 0
        return code, stdout.getvalue(), stderr.getvalue()
    return 0, stdout.getvalue(), stderr.getvalue()


class TestVersion(unittest.TestCase):
    def test_version_looks_semver(self):
        self.assertRegex(human_tester.__version__, r"^\d+\.\d+\.\d+")

    def test_version_flag_in_process(self):
        code, out, _ = run_main(["--version"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), human_tester.__version__)

    def test_version_flag_via_module_shortcut(self):
        proc = subprocess.run(
            [sys.executable, "-m", "human_tester", "--version"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), human_tester.__version__)

    def test_dist_version_matches_package(self):
        from importlib.metadata import PackageNotFoundError, version

        try:
            dist_version = version("human-like-ai-tester")
        except PackageNotFoundError:
            self.skipTest("package not installed in this interpreter")
        self.assertEqual(dist_version, human_tester.__version__)


class TestSubcommandStability(unittest.TestCase):
    def test_all_v020_subcommands_still_registered(self):
        code, out, _ = run_main([])
        self.assertEqual(code, 1)  # no subcommand -> usage + exit 1
        for sub in EXPECTED_SUBCOMMANDS:
            self.assertIn(sub, out, f"subcommand '{sub}' vanished from --help")

    def test_each_subcommand_has_help(self):
        for sub in EXPECTED_SUBCOMMANDS:
            code, out, _ = run_main([sub, "--help"])
            self.assertEqual(code, 0, f"'{sub} --help' failed")
            self.assertIn("usage:", out)

    def test_audit_offers_json_output(self):
        code, out, _ = run_main(["audit", "--help"])
        self.assertEqual(code, 0)
        self.assertIn("--json-output", out)


class TestCliErrors(unittest.TestCase):
    def test_validate_missing_file_exits_2_with_message(self):
        code, out, err = run_main(["validate-file", "definitely-missing-xyz.csv"])
        self.assertEqual(code, 2)
        self.assertIn("definitely-missing-xyz.csv", err)


if __name__ == "__main__":
    unittest.main()
