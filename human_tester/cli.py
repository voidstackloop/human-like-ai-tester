"""Command Line Interface for Human-Like AI Tester."""

import argparse
import sys
import threading
import time
from .personas import list_personas, get_persona
from .typo_engine import TypoEngine
from .cognitive_engine import CognitiveEngine
from .reporter import AuditReporter
from .paradigms import CLITester, APITester, WebTester, ChatTester, FileTester
from .mock_target_app import MockAppHandler
import http.server


def cmd_personas(args):
    """List available personas."""
    personas = list_personas()
    print("\n" + "=" * 60)
    print("  🧑 AVAILABLE HUMAN SIMULATION PERSONAS")
    print("=" * 60)
    for p in personas:
        print(f"\n[{p.id.upper()}] - {p.name}")
        print(f"  Archetype:     {p.archetype}")
        print(f"  Typing Speed:  {p.wpm} WPM (Typo Rate: {int(p.typo_rate * 100)}%)")
        print(f"  Patience:      {p.patience_seconds}s (Rage Click Prob: {int(p.rage_click_probability * 100)}%)")
        print(f"  Reading Depth: {p.reading_depth}")
        print(f"  Description:   {p.description}")
    print("\n" + "=" * 60 + "\n")


def cmd_simulate(args):
    """Simulate human typo stream on input text."""
    persona = get_persona(args.persona)
    engine = TypoEngine()
    print(f"\n[*] Simulating input for persona: {persona.name}")
    print(f"[*] Original text: '{args.text}'")

    for i in range(1, args.count + 1):
        corrupted = engine.introduce_typos(args.text, error_rate=persona.typo_rate)
        if args.clipboard:
            corrupted = engine.add_clipboard_quirks(corrupted)
        print(f"  Attempt {i}: {corrupted}")
    print()


def cmd_test_cli(args):
    """Test a CLI command with human behavior."""
    persona = get_persona(args.persona)
    reporter = AuditReporter("CLI: " + " ".join(args.target_command), persona.name)
    tester = CLITester(args.target_command, persona, reporter)

    print(f"\n[*] Initiating CLI Human Test with persona: {persona.name}")
    print(f"[*] Base Command: {' '.join(args.target_command)}")

    print("[1/3] Testing help discoverability (--help, -h)...")
    tester.test_help_and_discoverability()

    if args.flags:
        flags_list = [f.strip() for f in args.flags.split(",") if f.strip()]
        print(f"[2/3] Testing flag typos on: {flags_list}...")
        tester.test_flag_typos(flags_list)

    print("[3/3] Testing unquoted space in path arguments...")
    tester.test_unquoted_spaces_in_path()

    print("\n" + reporter.generate_markdown())


def cmd_test_web(args):
    """Test a web application with human behavior."""
    persona = get_persona(args.persona)
    reporter = AuditReporter(args.url, persona.name)
    tester = WebTester(args.url, persona, reporter)

    print(f"\n[*] Initiating Web Human Test on: {args.url}")
    print(f"[*] Persona: {persona.name}")

    print("[1/3] Measuring page load & cognitive patience threshold...")
    res = tester.test_page_load_and_clarity()
    print(f"      Load status: {res.get('status', 'err')}, time: {res.get('load_time_seconds')}s")

    if args.form_endpoint:
        print(f"[2/3] Testing form submission with human formatting...")
        sample_fields = {
            "name": "Jane O'Connor",
            "phone": "5551234567",
            "email": "jane@example.com",
            "amount": "100.00",
        }
        res_form = tester.test_form_submission_with_human_formatting(args.form_endpoint, sample_fields)
        print(f"      Form response status: {res_form.get('status')}")

        print(f"[3/3] Testing rapid double-click / rage click vulnerability...")
        res_double = tester.test_rapid_double_click_vulnerability(args.form_endpoint, sample_fields)
        print(f"      Double submit test responses: {res_double.get('responses')}")

    print("\n" + reporter.generate_markdown())


def cmd_test_api(args):
    """Test a REST API with human developer mistakes."""
    persona = get_persona(args.persona)
    reporter = AuditReporter(args.url, persona.name)
    tester = APITester(args.url, persona, reporter)

    print(f"\n[*] Initiating API Human Test on: {args.url}")
    print(f"[*] Persona: {persona.name}")

    print("[1/3] Testing trailing slashes...")
    tester.test_trailing_slashes(args.endpoint or "/")

    if args.endpoint:
        print(f"[2/3] Testing string instead of number on {args.endpoint}...")
        tester.test_string_instead_of_number(args.endpoint, "count", 42)

        print(f"[3/3] Testing unexpected additional payload fields...")
        tester.test_unexpected_payload_fields(args.endpoint, {"id": 1, "name": "Item"})

    print("\n" + reporter.generate_markdown())


def cmd_test_chat(args):
    """Generate human conversational test prompts."""
    persona = get_persona(args.persona)
    tester = ChatTester(persona)
    prompts = tester.generate_human_chat_prompts(args.intent or "support request")

    print(f"\n" + "=" * 60)
    print(f"  💬 HUMAN CONVERSATIONAL TEST VECTORS ({persona.name})")
    print("=" * 60)
    for p in prompts:
        print(f"\nPattern:     {p['pattern_id']}")
        print(f"Description: {p['description']}")
        print(f"Simulated:   \"{p['human_prompt']}\"")
    print("\n" + "=" * 60 + "\n")


def cmd_generate_file(args):
    """Generate realistic human-corrupted test file."""
    persona = get_persona(args.persona)
    tester = FileTester(persona)
    if args.type == "csv":
        content = tester.generate_human_csv(include_bom=not args.no_bom, mixed_delimiters=args.mixed)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[*] Human CSV written to: {args.output}")
        else:
            print(content)
    elif args.type == "json":
        content = tester.generate_human_json()
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[*] Human JSON written to: {args.output}")
        else:
            print(content)


def cmd_demo(args):
    """Launch mock server and run live end-to-end human simulation test."""
    port = args.port or 8989
    server = http.server.HTTPServer(("127.0.0.1", port), MockAppHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    print(f"\n🚀 [DEMO] Launched mock app with human UX traps at http://localhost:{port}/")
    time.sleep(0.5)

    persona = get_persona("rushed_commuter")
    reporter = AuditReporter(f"http://localhost:{port}", persona.name)
    web_tester = WebTester(f"http://localhost:{port}", persona, reporter)
    api_tester = APITester(f"http://localhost:{port}", persona, reporter)

    print(f"🧑 Running Human Test Simulation as: {persona.name} (Rushed Commuter)\n")

    # Step 1: Page load & patience
    print("  [Step 1] Loading checkout page...")
    web_tester.test_page_load_and_clarity()

    # Step 2: Form submission with human phone format: (555) 123-4567
    print("  [Step 2] Entering phone formatted with parentheses and dashes...")
    web_tester.test_form_submission_with_human_formatting(
        "/api/submit-order",
        {"name": "Alex O'Connor", "phone": "5551234567", "email": "alex@gmail.com", "amount": "49.99"},
    )

    # Step 3: Rapid double click
    print("  [Step 3] Submitting order and rage-clicking due to latency...")
    web_tester.test_rapid_double_click_vulnerability(
        "/api/submit-order",
        {"name": "Alex", "phone": "5551234567", "email": "alex@gmail.com", "amount": "49.99"},
    )

    # Step 4: API user string type
    print("  [Step 4] API test: passing age as string '25' instead of int 25...")
    api_tester.test_string_instead_of_number("/api/users", "age", 25)

    print("\n" + reporter.generate_markdown())
    server.shutdown()


def main():
    parser = argparse.ArgumentParser(
        description="Human-Like AI Tester: Multi-Paradigm Human Behavior Simulation Engine."
    )
    subparsers = parser.add_subparsers(dest="subcommand")

    # Subcommand: personas
    subparsers.add_parser("personas", help="List all available human personas")

    # Subcommand: simulate
    p_sim = subparsers.add_parser("simulate", help="Simulate human keystroke typos on a text string")
    p_sim.add_argument("text", help="Text to humanize")
    p_sim.add_argument("--persona", default="rushed_commuter", help="Persona ID")
    p_sim.add_argument("--count", type=int, default=3, help="Number of samples to generate")
    p_sim.add_argument("--clipboard", action="store_true", help="Include clipboard artifacts")

    # Subcommand: test-cli
    p_cli = subparsers.add_parser("test-cli", help="Test a CLI tool as a human user")
    p_cli.add_argument("target_command", nargs="+", help="Base command and arguments (e.g. git status)")
    p_cli.add_argument("--persona", default="rushed_commuter", help="Persona ID")
    p_cli.add_argument("--flags", help="Comma-separated list of flags to test typos on (e.g. '--version,--help')")

    # Subcommand: test-web
    p_web = subparsers.add_parser("test-web", help="Test a web app / form as a human user")
    p_web.add_argument("url", help="Target URL")
    p_web.add_argument("--form-endpoint", help="Relative form action endpoint to test")
    p_web.add_argument("--persona", default="rushed_commuter", help="Persona ID")

    # Subcommand: test-api
    p_api = subparsers.add_parser("test-api", help="Test an API endpoint with human integration mistakes")
    p_api.add_argument("url", help="Base API URL")
    p_api.add_argument("--endpoint", help="Specific endpoint path")
    p_api.add_argument("--persona", default="cynical_power_user", help="Persona ID")

    # Subcommand: test-chat
    p_chat = subparsers.add_parser("test-chat", help="Generate conversational human user test prompts")
    p_chat.add_argument("--intent", default="general", help="Core user intent")
    p_chat.add_argument("--persona", default="rushed_commuter", help="Persona ID")

    # Subcommand: generate-file
    p_file = subparsers.add_parser("generate-file", help="Generate a messy human file for ingestion tests")
    p_file.add_argument("type", choices=["csv", "json"], help="File format")
    p_file.add_argument("--output", "-o", help="Output file path")
    p_file.add_argument("--no-bom", action="store_true", help="Exclude Excel UTF-8 BOM")
    p_file.add_argument("--mixed", action="store_true", help="Include mixed delimiters")
    p_file.add_argument("--persona", default="fatigued_worker", help="Persona ID")

    # Subcommand: demo
    p_demo = subparsers.add_parser("demo", help="Run self-contained live demo with flawed mock app")
    p_demo.add_argument("--port", type=int, default=8989, help="Port to run mock app")

    args = parser.parse_args()

    if not args.subcommand:
        parser.print_help()
        sys.exit(1)

    if args.subcommand == "personas":
        cmd_personas(args)
    elif args.subcommand == "simulate":
        cmd_simulate(args)
    elif args.subcommand == "test-cli":
        cmd_test_cli(args)
    elif args.subcommand == "test-web":
        cmd_test_web(args)
    elif args.subcommand == "test-api":
        cmd_test_api(args)
    elif args.subcommand == "test-chat":
        cmd_test_chat(args)
    elif args.subcommand == "generate-file":
        cmd_generate_file(args)
    elif args.subcommand == "demo":
        cmd_demo(args)


if __name__ == "__main__":
    main()
