"""Enrichment tests: new personas, vectors, desktop/mobile testers, heuristics.

Network-free: live HTTP checks are covered by the mock-server demo instead.
"""

import sys
import unittest
from human_tester.personas import (
    get_persona, list_personas, personas_for_paradigm, describe_persona,
    RUSHED_COMMUTER, IMPATIENT_TEEN,
)
from human_tester.typo_engine import TypoEngine
from human_tester.cognitive_engine import CognitiveEngine
from human_tester.reporter import AuditReporter
from human_tester.error_patterns import all_vectors, ACCESSIBILITY_BARRIERS, I18N_LOCALE_TRAPS
from human_tester.agent_prompts import build_paradigm_prompt, sample_monologue
from human_tester.paradigms import (
    CLITester, ChatTester, FileTester, DesktopTester, MobileTester, WebTester, APITester,
)


class TestEnrichedPersonas(unittest.TestCase):
    def test_catalog_has_eight_personas(self):
        self.assertGreaterEqual(len(list_personas()), 8)

    def test_new_personas_retrievable(self):
        self.assertEqual(get_persona("accessibility_navigator").id, "accessibility_navigator")
        self.assertEqual(get_persona("non_native_speaker").id, "non_native_speaker")
        self.assertEqual(get_persona("impatient_teen").id, "impatient_teen")

    def test_impatient_teen_is_most_impatient(self):
        teens = get_persona("impatient_teen")
        others = [p for p in list_personas() if p.id != "impatient_teen"]
        self.assertTrue(all(teens.patience_seconds <= p.patience_seconds for p in others))

    def test_personas_for_paradigm(self):
        web = personas_for_paradigm("web")
        self.assertGreaterEqual(len(web), 2)
        self.assertIn("rushed_commuter", [p.id for p in web])
        self.assertEqual(len(personas_for_paradigm("zzz")), len(list_personas()))

    def test_describe_persona(self):
        summary = describe_persona("rushed_commuter")
        self.assertIn("Alex", summary)
        self.assertIn("WPM", summary)


class TestEnrichedTypoEngine(unittest.TestCase):
    def setUp(self):
        self.engine = TypoEngine(seed=7)

    def test_autocorrect_fail(self):
        out = self.engine.introduce_autocorrect_fail("lets plan a meeting tomorrow")
        self.assertNotEqual(out, "lets plan a meeting tomorrow")

    def test_autocorrect_no_candidate_unchanged(self):
        self.assertEqual(self.engine.introduce_autocorrect_fail("xyzzy qqq"), "xyzzy qqq")

    def test_voice_transcription(self):
        out = self.engine.introduce_voice_transcription_errors("Their account is here for you")
        self.assertEqual(out, out.lower())
        self.assertNotEqual(out, "Their account is here for you")

    def test_phonetic_spelling(self):
        out = self.engine.introduce_phonetic_spelling("My phone number and address please")
        self.assertIn("fone", out)
        self.assertIn("adress", out)

    def test_password_paste_varies(self):
        variants = {self.engine.corrupt_password_paste("hunter2!") for _ in range(12)}
        self.assertGreater(len(variants), 1)

    def test_url_bar_corruption(self):
        out = self.engine.corrupt_url_bar("https://example.com/shop")
        self.assertNotEqual(out, "https://example.com/shop")

    def test_date_formatting(self):
        out = self.engine.format_date_human_style(2026, 5, 12)
        self.assertIn("2026", out)

    def test_credit_card_digits_preserved(self):
        out = self.engine.format_credit_card_human_style("4111111111111111")
        self.assertEqual("".join(c for c in out if c.isdigit()), "4111111111111111")


class TestEnrichedCognitiveEngine(unittest.TestCase):
    def setUp(self):
        self.cog = CognitiveEngine(RUSHED_COMMUTER)

    def test_interruption(self):
        res = self.cog.simulate_interruption()
        self.assertIn("pause_seconds", res)
        self.assertGreaterEqual(res["pause_seconds"], 8.0)
        self.assertGreater(self.cog.frustration_score, 0.0)

    def test_attention_decay_grows(self):
        early = self.cog.attention_decay(0, 6)
        late = self.cog.attention_decay(5, 6)
        self.assertLessEqual(early, 1.2)
        self.assertGreater(late, early)

    def test_retry_learning(self):
        import random
        random.seed(11)
        before = self.cog.calculate_typing_delay_seconds(100)
        self.cog.frustration_score = 30.0
        self.cog.second_attempt_speedup()
        self.assertEqual(self.cog.retry_count, 1)
        self.assertLess(self.cog.frustration_score, 30.0)
        random.seed(11)  # same jitter draw -> retry must be strictly faster
        self.assertLess(self.cog.calculate_typing_delay_seconds(100), before)

    def test_scroll_fatigue_no_scroll(self):
        self.assertFalse(self.cog.scroll_fatigue_check(False))

    def test_record_success_relief(self):
        self.cog.frustration_score = 40.0
        self.cog.record_success()
        self.assertLess(self.cog.frustration_score, 40.0)


class TestEnrichedReporter(unittest.TestCase):
    def test_sync_frustration_keeps_max(self):
        r = AuditReporter("App", "Alex")
        r.sync_frustration(30.0)
        r.sync_frustration(10.0)
        self.assertEqual(r.frustration_score, 30.0)

    def test_severity_counts_and_plan(self):
        r = AuditReporter("App", "Alex")
        r.add_finding("FRICTION", "Cat", "Minor", "d", "a", "s", "fix")
        r.add_finding("CRITICAL", "Cat", "Major", "d", "a", "s", "fix now")
        counts = r.severity_counts()
        self.assertEqual(counts["CRITICAL"], 1)
        self.assertEqual(counts["FRICTION"], 1)
        plan = r.generate_remediation_plan()
        self.assertLess(plan.index("Major"), plan.index("Minor"))

    def test_dedupe_findings(self):
        r = AuditReporter("App", "sweep")
        for _ in range(3):
            r.add_finding("CRITICAL", "Cat", "Same bug", "d", "a", "s", "fix")
        r.add_finding("FRICTION", "Cat", "Other", "d", "a", "s", "fix")
        removed = r.dedupe_findings()
        self.assertEqual(removed, 2)
        self.assertEqual(len(r.findings), 2)
        self.assertIn("×3 personas", r.findings[0].title)

    def test_verdict_method(self):
        r = AuditReporter("App", "Alex")
        self.assertIn("PASS", r.verdict())
        r.add_finding("CRITICAL", "Cat", "X", "d", "a", "s", "fix")
        self.assertIn("CRITICAL", r.verdict())


class TestErrorPatternCatalog(unittest.TestCase):
    def test_all_vectors_categories(self):
        vectors = all_vectors()
        for key in ("passwords", "search", "urls", "credit_cards", "i18n_traps",
                    "accessibility", "mobile", "desktop", "api"):
            self.assertIn(key, vectors)
            self.assertTrue(vectors[key])
        self.assertTrue(ACCESSIBILITY_BARRIERS)
        self.assertTrue(I18N_LOCALE_TRAPS)


class TestAgentPrompts(unittest.TestCase):
    def test_paradigm_prompt(self):
        prompt = build_paradigm_prompt("mobile", "impatient_teen")
        self.assertIn("Zoe", prompt)
        self.assertIn("MOBILE", prompt)
        self.assertIn("Frustration", prompt)

    def test_sample_monologue(self):
        self.assertTrue(isinstance(sample_monologue(), str))


class TestDesktopTester(unittest.TestCase):
    def setUp(self):
        self.tester = DesktopTester("TestApp", get_persona("tech_novice"))

    def test_button_proximity_flags_close_pair(self):
        res = self.tester.audit_button_proximity(distance_px=12.0)
        self.assertTrue(res["risky"])
        self.assertEqual(len(self.tester.reporter.findings), 1)

    def test_button_proximity_passes_wide_gap(self):
        res = self.tester.audit_button_proximity(distance_px=120.0)
        self.assertFalse(res["risky"])

    def test_resize_clip(self):
        res = self.tester.simulate_window_resize([1280, 800], clipped_at=[800])
        self.assertTrue(res[800]["clipped"])
        self.assertFalse(res[1280]["clipped"])

    def test_dialog_half_state_critical(self):
        self.tester.simulate_dialog_cancel_midway("Save As", leaves_half_state=True)
        self.assertEqual(self.tester.reporter.findings[-1].severity, "CRITICAL")

    def test_shortcut_and_drop(self):
        self.tester.simulate_shortcut_misuse("Ctrl+S", collides_with_os=True)
        self.tester.simulate_drag_drop_miss(32, missed=True)
        self.assertEqual(len(self.tester.reporter.findings), 2)

    def test_manual_script(self):
        self.assertEqual(len(self.tester.generate_manual_script()), 7)


class TestMobileTester(unittest.TestCase):
    def setUp(self):
        self.tester = MobileTester("TestApp", get_persona("rushed_commuter"))

    def test_thumb_dead_zone(self):
        res = self.tester.audit_thumb_reach("top-right")
        self.assertTrue(res["unreachable_one_handed"])

    def test_thumb_safe_zone(self):
        res = self.tester.audit_thumb_reach("bottom-center")
        self.assertFalse(res["unreachable_one_handed"])

    def test_keyboard_overlap_critical(self):
        self.tester.audit_keyboard_overlap(submit_visible_with_keyboard=False)
        self.assertEqual(self.tester.reporter.findings[-1].severity, "CRITICAL")

    def test_rotation_wipe(self):
        res = self.tester.test_orientation_flip(state_preserved=False)
        self.assertFalse(res["state_preserved"])

    def test_deep_link_and_permission(self):
        self.tester.test_deep_link("myapp://order/7", cold_start_ok=True, preserves_context=False)
        self.tester.audit_permission_dialog("camera", rationale_shown=False, graceful_denial=True)
        self.assertEqual(len(self.tester.reporter.findings), 2)

    def test_rage_tap(self):
        res = self.tester.simulate_rage_tap(5.0)
        self.assertIn("did_rage_tap", res)

    def test_manual_script(self):
        self.assertEqual(len(self.tester.generate_manual_script()), 6)


class TestWebHeuristics(unittest.TestCase):
    def setUp(self):
        self.tester = WebTester("http://localhost:9", RUSHED_COMMUTER)

    def test_validation_wipe_critical(self):
        res = self.tester.audit_validation_state_preservation(
            {"name": "Alex", "phone": "555"}, {"name": "", "phone": ""})
        self.assertEqual(res["wiped_fields"], ["name", "phone"])
        self.assertEqual(self.tester.reporter.findings[-1].severity, "CRITICAL")

    def test_back_button_loss(self):
        res = self.tester.audit_back_button_state({"a": "x"}, {"a": ""})
        self.assertFalse(res["preserved"])

    def test_error_hidden_flag(self):
        res = self.tester.audit_error_visibility("top", "bottom")
        self.assertTrue(res["hidden"])
        res2 = self.tester.audit_error_visibility("inline", "bottom")
        self.assertFalse(res2["hidden"])


class TestAPITesterOffline(unittest.TestCase):
    def test_unreachable_host_graceful(self):
        tester = APITester("http://127.0.0.1:9", get_persona("cynical_power_user"))
        res = tester.test_trailing_slashes("/items")
        self.assertEqual(res["no_slash"], 0)
        self.assertEqual(res["with_slash"], 0)
        self.assertEqual(len(tester.reporter.findings), 0)


class TestCLITesterEnriched(unittest.TestCase):
    def test_empty_enter_colloquial_runs(self):
        tester = CLITester(["echo", "hi"], RUSHED_COMMUTER)
        results = tester.test_empty_enter_and_colloquial()
        self.assertEqual(len(results), 8)

    def test_ctrl_c_graceful(self):
        tester = CLITester([sys.executable, "-c", "import time; time.sleep(30)"], RUSHED_COMMUTER)
        res = tester.test_ctrl_c_during_long_run(wait_before_sigint=0.3)
        self.assertTrue(res.get("graceful", False))

    def test_empty_args(self):
        tester = CLITester(["echo", "hi"], RUSHED_COMMUTER)
        res = tester.test_extra_whitespace_and_empty_args()
        self.assertEqual(res["returncode"], 0)


class TestChatEnriched(unittest.TestCase):
    def test_ten_patterns(self):
        tester = ChatTester(IMPATIENT_TEEN)
        prompts = tester.generate_human_chat_prompts("support")
        ids = {p["pattern_id"] for p in prompts}
        self.assertGreaterEqual(len(prompts), 10)
        self.assertIn("voice_transcription_garble", ids)
        self.assertIn("all_caps_frustration", ids)

    def test_voice_prompts_lowercase(self):
        tester = ChatTester(IMPATIENT_TEEN)
        prompts = tester.generate_voice_prompts("support")
        self.assertGreaterEqual(len(prompts), 10)
        for p in prompts[:3]:
            self.assertEqual(p["human_prompt"], p["human_prompt"].lower())

    def test_empathy_check(self):
        tester = ChatTester(IMPATIENT_TEEN)
        cold = tester.evaluate_empathy("Error 500. Try again later.")
        self.assertFalse(cold["empathetic"])
        warm = tester.evaluate_empathy("Sorry this keeps failing — let me help you fix it.")
        self.assertTrue(warm["empathetic"])


class TestFileEnriched(unittest.TestCase):
    def test_tsv_generation(self):
        tester = FileTester(get_persona("fatigued_worker"))
        tsv = tester.generate_human_tsv()
        self.assertIn("\t", tsv)

    def test_header_case_variants(self):
        tester = FileTester(get_persona("fatigued_worker"))
        variants = tester.generate_header_case_variants()
        self.assertEqual(len(variants), 4)

    def test_validate_generated_csv_finds_traps(self):
        tester = FileTester(get_persona("fatigued_worker"))
        csv_text = tester.generate_human_csv(include_bom=True)
        result = tester.validate_csv_robustness(csv_text)
        ids = {t["id"] for t in result["traps"]}
        self.assertIn("bom", ids)
        self.assertIn("blank_rows", ids)
        self.assertIn("column_mismatch", ids)
        self.assertGreaterEqual(result["trap_count"], 3)

    def test_validate_clean_csv_no_traps(self):
        tester = FileTester(get_persona("fatigued_worker"))
        result = tester.validate_csv_robustness("a,b\n1,2")
        self.assertEqual(result["trap_count"], 0)


if __name__ == "__main__":
    unittest.main()
