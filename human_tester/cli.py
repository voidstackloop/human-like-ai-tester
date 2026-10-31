"""Command Line Interface for Human-Like AI Tester."""

import argparse
import sys
import threading
import time
from typing import List, Optional
from . import __version__
from .personas import list_personas, get_persona, describe_persona
from .typo_engine import TypoEngine
from .reporter import AuditReporter
from .paradigms import CLITester, APITester, WebTester, ChatTester, FileTester, DesktopTester, MobileTester
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
    if args.voice:
        print(f"  Voice-dictated: {engine.introduce_voice_transcription_errors(args.text)}")
    if args.autocorrect:
        print(f"  Autocorrect-fail: {engine.introduce_autocorrect_fail(args.text)}")
    if args.phonetic:
        print(f"  Phonetic (ESL): {engine.introduce_phonetic_spelling(args.text)}")
    print()


def cmd_test_cli(args):
    """Test a CLI command with human behavior."""
    persona = get_persona(args.persona)
    reporter = AuditReporter("CLI: " + " ".join(args.target_command), persona.name)
    tester = CLITester(args.target_command, persona, reporter)

    print(f"\n[*] Initiating CLI Human Test with persona: {persona.name}")
    print(f"[*] Base Command: {' '.join(args.target_command)}")

    print("[1/5] Testing help discoverability (--help, -h)...")
    tester.test_help_and_discoverability()

    if args.flags:
        flags_list = [f.strip() for f in args.flags.split(",") if f.strip()]
        print(f"[2/5] Testing flag typos on: {flags_list}...")
        tester.test_flag_typos(flags_list)

    print("[3/5] Testing unquoted space in path arguments...")
    tester.test_unquoted_spaces_in_path()

    print("[4/5] Testing bare Enter + colloquial prompt answers...")
    tester.test_empty_enter_and_colloquial()

    print("[5/5] Testing Ctrl-C handling + paste-artifact args...")
    tester.test_ctrl_c_during_long_run()
    tester.test_extra_whitespace_and_empty_args()

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
        print("[2/3] Testing form submission with human formatting...")
        sample_fields = {
            "name": "Jane O'Connor",
            "phone": "5551234567",
            "email": "jane@example.com",
            "amount": "100.00",
        }
        res_form = tester.test_form_submission_with_human_formatting(args.form_endpoint, sample_fields)
        print(f"      Form response status: {res_form.get('status')}")

        print("[3/3] Testing rapid double-click / rage click vulnerability...")
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

    print("[1/5] Testing trailing slashes...")
    tester.test_trailing_slashes(args.endpoint or "/")

    if args.endpoint:
        print(f"[2/5] Testing string instead of number on {args.endpoint}...")
        tester.test_string_instead_of_number(args.endpoint, "count", 42)

        print(f"[3/5] Testing boolean-as-string on {args.endpoint}...")
        tester.test_boolean_as_string(args.endpoint, "active")

        print("[4/5] Testing unexpected additional payload fields...")
        tester.test_unexpected_payload_fields(args.endpoint, {"id": 1, "name": "Item"})

        print("[5/5] Testing pagination misuse + webhook retry...")
        tester.test_pagination_misuse(args.endpoint)
        tester.test_webhook_retry(args.endpoint)

    if args.graphql_endpoint:
        print(f"[6/6] Testing GraphQL typo field on {args.graphql_endpoint}...")
        tester.test_graphql_typo_field(args.graphql_endpoint)

    print("\n" + reporter.generate_markdown())


def cmd_test_chat(args):
    """Generate human conversational test prompts."""
    persona = get_persona(args.persona)
    tester = ChatTester(persona)
    if args.voice:
        prompts = tester.generate_voice_prompts(args.intent or "support request")
        label = "VOICE-DICTATED"
    else:
        prompts = tester.generate_human_chat_prompts(args.intent or "support request")
        label = "HUMAN CONVERSATIONAL TEST VECTORS"

    print("\n" + "=" * 60)
    print(f"  💬 {label} ({persona.name})")
    print("=" * 60)
    for p in prompts:
        print(f"\nPattern:     {p['pattern_id']}")
        print(f"Description: {p['description']}")
        print(f"Simulated:   \"{p['human_prompt']}\"")
    if args.reply:
        print("\n--- Evaluating assistant reply ---")
        verdict = tester.evaluate_assistant_response("vague_complaint", args.reply)
        empathy = tester.evaluate_empathy(args.reply)
        print(f"Handled gracefully: {verdict['handled_gracefully']}")
        print(f"Empathetic: {empathy['empathetic']}")
    print("\n" + "=" * 60 + "\n")


def cmd_test_desktop(args):
    """Heuristic desktop GUI audit from supplied layout metadata."""
    persona = get_persona(args.persona)
    reporter = AuditReporter(f"Desktop: {args.app_name}", persona.name)
    tester = DesktopTester(args.app_name, persona, reporter)

    print(f"\n[*] Desktop GUI Human Audit: {args.app_name} as {persona.name}")
    tester.audit_button_proximity(distance_px=args.cancel_distance_px)
    widths = [int(w) for w in args.breakpoints.split(",") if w.strip()]
    clipped = [int(w) for w in (args.clipped_at or "").split(",") if w.strip()]
    tester.simulate_window_resize(widths, clipped)
    if args.dialog:
        tester.simulate_dialog_cancel_midway(args.dialog, leaves_half_state=args.dialog_half_state)
    tester.simulate_shortcut_misuse(args.shortcut, collides_with_os=args.shortcut_collision)
    tester.simulate_drag_drop_miss(args.drop_target_px, missed=args.drop_missed)
    reporter.sync_frustration(tester.cognitive.frustration_score)

    print("\n[*] Manual walkthrough script:")
    for step in tester.generate_manual_script():
        print(f"  {step}")
    print("\n" + reporter.generate_markdown())


def cmd_test_mobile(args):
    """Heuristic mobile/touch audit from supplied layout metadata."""
    persona = get_persona(args.persona)
    reporter = AuditReporter(f"Mobile: {args.app_name}", persona.name)
    tester = MobileTester(args.app_name, persona, reporter)

    print(f"\n[*] Mobile Human Audit: {args.app_name} as {persona.name}")
    tester.audit_thumb_reach(args.action_position)
    tester.audit_keyboard_overlap(submit_visible_with_keyboard=not args.keyboard_covered)
    tester.test_orientation_flip(state_preserved=not args.rotation_wipes)
    if args.deep_link:
        tester.test_deep_link(args.deep_link, cold_start_ok=not args.deep_link_broken,
                              preserves_context=not args.deep_link_broken)
    tester.audit_permission_dialog(args.permission, rationale_shown=not args.no_rationale,
                                   graceful_denial=not args.deny_crashes)
    rage = tester.simulate_rage_tap(args.slow_response)
    print(f"[*] Rage-tap check ({args.slow_response}s response): {rage['tap_count']} taps")

    print("\n[*] Manual walkthrough script:")
    for step in tester.generate_manual_script():
        print(f"  {step}")
    print("\n" + reporter.generate_markdown())


def cmd_validate_file(args):
    """Audit a real file on disk for human-ingestion traps."""
    persona = get_persona(args.persona)
    tester = FileTester(persona)
    try:
        with open(args.path, "r", encoding="utf-8-sig") as f:
            raw = f.read()
        # Re-add BOM marker for the audit if the file had one (utf-8-sig strips it).
        with open(args.path, "rb") as f:
            had_bom = f.read(3) == b"\xef\xbb\xbf"
    except OSError as exc:
        print(f"[!] Cannot read file '{args.path}': {exc.strerror or exc}", file=sys.stderr)
        sys.exit(2)
    result = tester.validate_csv_robustness(("\ufeff" if had_bom else "") + raw)
    print(f"\n[*] Validated {args.path}: {result['trap_count']} trap(s) found")
    for t in result["traps"]:
        print(f"  - [{t['id']}] {t['detail']}")
    print("\n" + tester.reporter.generate_markdown())


def cmd_audit(args):
    """Multi-persona sweep: web + API checks across several personas, one report."""
    persona_ids = [p.strip() for p in args.personas.split(",") if p.strip()]
    reporter = AuditReporter(f"AUDIT: {args.url}", "multi-persona sweep")
    print(f"\n[*] Multi-persona audit of {args.url} with: {', '.join(persona_ids)}")
    for pid in persona_ids:
        persona = get_persona(pid)
        print(f"\n--- Persona: {describe_persona(pid)} ---")
        web = WebTester(args.url, persona, reporter)
        res = web.test_page_load_and_clarity()
        print(f"    load: {res.get('status', 'err')} in {res.get('load_time_seconds')}s")
        if args.form_endpoint:
            fields = {"name": "Jane O'Connor", "phone": "5551234567",
                      "email": "jane@example.com", "amount": "100.00"}
            rf = web.test_form_submission_with_human_formatting(args.form_endpoint, fields)
            print(f"    form: HTTP {rf.get('status')}")
            rd = web.test_rapid_double_click_vulnerability(args.form_endpoint, fields)
            print(f"    double-submit: {rd.get('responses')}")
        api = APITester(args.url, persona, reporter)
        api.test_trailing_slashes(args.endpoint or "/")
        if args.endpoint:
            api.test_string_instead_of_number(args.endpoint, "count", 42)
            api.test_boolean_as_string(args.endpoint, "active")
        reporter.sync_frustration(web.cognitive.frustration_score)
    deduped = reporter.dedupe_findings()
    if deduped:
        print(f"\n[*] Merged {deduped} duplicate finding(s) across personas")
    if args.output:
        reporter.save_markdown(args.output)
        print(f"\n[*] Report saved to {args.output}")
    if args.json_output:
        reporter.save_json(args.json_output)
        print(f"\n[*] JSON report saved to {args.json_output}")
    print("\n" + reporter.generate_markdown())


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
    elif args.type == "tsv":
        content = tester.generate_human_tsv()
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[*] Human TSV written to: {args.output}")
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

    # Step 5: Validation state loss (heuristic)
    print("  [Step 5] Checking validation error state preservation...")
    web_tester.audit_validation_state_preservation(
        {"name": "Alex", "phone": "(555) 123-4567", "email": "alex@gmail.com"},
        {"name": "", "phone": "", "email": ""},
    )
    reporter.sync_frustration(web_tester.cognitive.frustration_score)

    print("\n" + reporter.generate_markdown())
    server.shutdown()


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        description="Human-Like AI Tester: Multi-Paradigm Human Behavior Simulation Engine."
    )
    parser.add_argument("--version", action="store_true", help="Show the package version and exit")
    subparsers = parser.add_subparsers(dest="subcommand")

    # Subcommand: personas
    subparsers.add_parser("personas", help="List all available human personas")

    # Subcommand: simulate
    p_sim = subparsers.add_parser("simulate", help="Simulate human keystroke typos on a text string")
    p_sim.add_argument("text", help="Text to humanize")
    p_sim.add_argument("--persona", default="rushed_commuter", help="Persona ID")
    p_sim.add_argument("--count", type=int, default=3, help="Number of samples to generate")
    p_sim.add_argument("--clipboard", action="store_true", help="Include clipboard artifacts")
    p_sim.add_argument("--voice", action="store_true", help="Also show voice-dictation variant")
    p_sim.add_argument("--autocorrect", action="store_true", help="Also show autocorrect-fail variant")
    p_sim.add_argument("--phonetic", action="store_true", help="Also show ESL phonetic-spelling variant")

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
    p_api.add_argument("--graphql-endpoint", help="GraphQL endpoint path for typo-field test")
    p_api.add_argument("--persona", default="cynical_power_user", help="Persona ID")

    # Subcommand: test-chat
    p_chat = subparsers.add_parser("test-chat", help="Generate conversational human user test prompts")
    p_chat.add_argument("--intent", default="general", help="Core user intent")
    p_chat.add_argument("--persona", default="rushed_commuter", help="Persona ID")
    p_chat.add_argument("--voice", action="store_true", help="Generate voice-dictated variants")
    p_chat.add_argument("--reply", help="Assistant reply to evaluate for grace + empathy")

    # Subcommand: test-desktop
    p_desk = subparsers.add_parser("test-desktop", help="Heuristic desktop GUI audit from layout metadata")
    p_desk.add_argument("app_name", help="Application name under test")
    p_desk.add_argument("--persona", default="tech_novice", help="Persona ID")
    p_desk.add_argument("--cancel-distance-px", type=float, default=100.0, help="Cancel/Submit gap in px")
    p_desk.add_argument("--breakpoints", default="1280,1024,800", help="Window widths to check")
    p_desk.add_argument("--clipped-at", default="", help="Widths where submit clips, e.g. '800'")
    p_desk.add_argument("--dialog", help="Dialog name to test Cancel-atomicity on")
    p_desk.add_argument("--dialog-half-state", action="store_true", help="Cancel leaves half-applied state")
    p_desk.add_argument("--shortcut", default="Ctrl+S", help="App shortcut to collision-check")
    p_desk.add_argument("--shortcut-collision", action="store_true", help="Shortcut collides with OS default")
    p_desk.add_argument("--drop-target-px", type=float, default=96.0, help="Drop target size in px")
    p_desk.add_argument("--drop-missed", action="store_true", help="A missed drop fails silently")

    # Subcommand: test-mobile
    p_mob = subparsers.add_parser("test-mobile", help="Heuristic mobile/touch audit from layout metadata")
    p_mob.add_argument("app_name", help="Application name under test")
    p_mob.add_argument("--persona", default="rushed_commuter", help="Persona ID")
    p_mob.add_argument("--action-position", default="bottom-center", help="Primary action position (e.g. top-right)")
    p_mob.add_argument("--keyboard-covered", action="store_true", help="Keyboard covers submit/errors")
    p_mob.add_argument("--rotation-wipes", action="store_true", help="Rotation wipes form state")
    p_mob.add_argument("--deep-link", help="Deep link URL to verify")
    p_mob.add_argument("--deep-link-broken", action="store_true", help="Deep link drops context")
    p_mob.add_argument("--permission", default="camera", help="Permission to audit")
    p_mob.add_argument("--no-rationale", action="store_true", help="No pre-prompt rationale shown")
    p_mob.add_argument("--deny-crashes", action="store_true", help="Denying dead-ends the flow")
    p_mob.add_argument("--slow-response", type=float, default=3.0, help="Slow button latency for rage-tap check")

    # Subcommand: validate-file
    p_val = subparsers.add_parser("validate-file", help="Audit a real CSV file for human-ingestion traps")
    p_val.add_argument("path", help="Path to the CSV file")
    p_val.add_argument("--persona", default="fatigued_worker", help="Persona ID")

    # Subcommand: audit (multi-persona sweep)
    p_audit = subparsers.add_parser("audit", help="Multi-persona web+API sweep with one merged report")
    p_audit.add_argument("url", help="Target base URL")
    p_audit.add_argument("--endpoint", help="API endpoint path for type-coercion checks")
    p_audit.add_argument("--form-endpoint", help="Relative form action endpoint to test")
    p_audit.add_argument("--personas", default="rushed_commuter,tech_novice,impatient_teen",
                         help="Comma-separated persona IDs")
    p_audit.add_argument("--output", "-o", help="Write merged markdown report to file")
    p_audit.add_argument("--json-output", help="Write merged JSON report to file (for CI pipelines)")

    # Subcommand: generate-file
    p_file = subparsers.add_parser("generate-file", help="Generate a messy human file for ingestion tests")
    p_file.add_argument("type", choices=["csv", "json", "tsv"], help="File format")
    p_file.add_argument("--output", "-o", help="Output file path")
    p_file.add_argument("--no-bom", action="store_true", help="Exclude Excel UTF-8 BOM")
    p_file.add_argument("--mixed", action="store_true", help="Include mixed delimiters")
    p_file.add_argument("--persona", default="fatigued_worker", help="Persona ID")

    # Subcommand: demo
    p_demo = subparsers.add_parser("demo", help="Run self-contained live demo with flawed mock app")
    p_demo.add_argument("--port", type=int, default=8989, help="Port to run mock app")

    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        return

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
    elif args.subcommand == "test-desktop":
        cmd_test_desktop(args)
    elif args.subcommand == "test-mobile":
        cmd_test_mobile(args)
    elif args.subcommand == "validate-file":
        cmd_validate_file(args)
    elif args.subcommand == "audit":
        cmd_audit(args)
    elif args.subcommand == "generate-file":
        cmd_generate_file(args)
    elif args.subcommand == "demo":
        cmd_demo(args)


if __name__ == "__main__":
    main()
