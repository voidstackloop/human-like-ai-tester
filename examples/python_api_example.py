#!/usr/bin/env python3
"""Library usage example: use human-like-ai-tester as a Python API (no CLI).

Run from the repo root:

    python examples/python_api_example.py

Network-free: everything below runs locally with zero dependencies.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from human_tester import (  # noqa: E402
    AuditReporter,
    CognitiveEngine,
    TypoEngine,
    describe_persona,
    get_persona,
    list_personas,
    personas_for_paradigm,
)
from human_tester.paradigms import ChatTester, FileTester  # noqa: E402


def main() -> None:
    # 1. Pick a persona -----------------------------------------------------
    print(f"Personas available: {len(list_personas())}")
    persona = get_persona("rushed_commuter")
    print("Using:", describe_persona("rushed_commuter"))
    print("Recommended for web:", [p.id for p in personas_for_paradigm("web")])

    # 2. Humanize input -----------------------------------------------------
    typos = TypoEngine(seed=42)  # seed for reproducible demos
    text = "Lets plan a meeting tomorrow"
    print("\nOriginal:   ", text)
    print("With typos: ", typos.introduce_typos(text, error_rate=persona.typo_rate))
    print("Autocorrect:", typos.introduce_autocorrect_fail("lets plan a meeting tomorrow"))
    print("Voice dict: ", typos.introduce_voice_transcription_errors("Their account is here"))
    print("Phonetic:   ", typos.introduce_phonetic_spelling("My phone number and address please"))
    print("Phone style:", typos.format_phone_human_style("5551234567"))

    # 3. Model impatience ---------------------------------------------------
    mind = CognitiveEngine(persona)
    print(f"\nReading 30 words takes ~{mind.calculate_reading_delay_seconds(30)}s")
    rage, clicks, _ = mind.trigger_rage_click_check(3.5)
    print(f"After a 3.5s hang: rage_click={rage} ({clicks} clicks), "
          f"frustration={mind.frustration_score:.1f} ({mind.get_frustration_level()})")

    # 4. Chatbot test vectors -----------------------------------------------
    chat = ChatTester(persona)
    prompts = chat.generate_human_chat_prompts("cancel my order")
    print(f"\nGenerated {len(prompts)} human chat prompts, e.g.:")
    print(f"  [{prompts[0]['pattern_id']}] \"{prompts[0]['human_prompt']}\"")

    # 5. Messy files: generate one, then audit it ----------------------------
    files = FileTester(persona)
    messy_csv = files.generate_human_csv(include_bom=True, mixed_delimiters=True)
    verdict = files.validate_csv_robustness(messy_csv)
    print(f"\nMessy CSV audit: {verdict['trap_count']} trap(s) found")
    for trap in verdict["traps"][:3]:
        print(f"  - [{trap['id']}] {trap['detail']}")

    # 6. Compile a report ----------------------------------------------------
    reporter = AuditReporter("demo-checkout", persona.name)
    reporter.add_finding(
        severity="FRICTION",
        category="Formatting",
        title="Phone field rejects (555) 123-4567",
        description="Rushed users type formatted numbers; strict digit fields bounce them.",
        simulated_action="Typed (555) 123-4567 into the phone field",
        system_reaction="Validation error: 'Numbers only'",
        recommendation="Strip formatting characters server-side before validating.",
    )
    reporter.sync_frustration(mind.frustration_score)
    print(f"\nReport verdict: {reporter.verdict()} "
          f"(counts: {reporter.severity_counts()})")


if __name__ == "__main__":
    main()
