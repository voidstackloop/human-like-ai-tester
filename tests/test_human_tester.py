"""Unit tests for the Universal Human-Like AI Tester."""

import unittest
from human_tester.personas import get_persona, list_personas, RUSHED_COMMUTER
from human_tester.typo_engine import TypoEngine
from human_tester.cognitive_engine import CognitiveEngine
from human_tester.reporter import AuditReporter
from human_tester.paradigms import ChatTester, FileTester


class TestHumanTesterCore(unittest.TestCase):

    def setUp(self):
        self.typo_engine = TypoEngine(seed=42)
        self.persona = RUSHED_COMMUTER
        self.cognitive = CognitiveEngine(self.persona)

    def test_personas_registry(self):
        personas = list_personas()
        self.assertGreaterEqual(len(personas), 5)
        p = get_persona("rushed_commuter")
        self.assertEqual(p.id, "rushed_commuter")
        self.assertEqual(p.reading_depth, "skims")

    def test_adjacent_key_slip(self):
        char = "g"
        slipped = self.typo_engine.apply_adjacent_key_slip(char)
        self.assertIn(slipped, ['f', 't', 'y', 'h', 'b', 'v'])

    def test_transposition(self):
        word = "the"
        transposed = self.typo_engine.introduce_transposition(word)
        self.assertIn(transposed, ["hte", "teh"])

    def test_omission(self):
        word = "committee"
        omitted = self.typo_engine.introduce_omission(word)
        self.assertEqual(len(omitted), len(word) - 1)

    def test_fat_finger(self):
        word = "book"
        fat_fingered = self.typo_engine.introduce_fat_finger(word)
        self.assertEqual(len(fat_fingered), len(word) + 1)

    def test_phone_human_formatting(self):
        phone = "5551234567"
        formatted = self.typo_engine.format_phone_human_style(phone)
        self.assertTrue("-" in formatted or "(" in formatted or "." in formatted or " " in formatted)

    def test_currency_human_formatting(self):
        amt = 1250.50
        formatted = self.typo_engine.format_currency_human_style(amt)
        self.assertTrue(
            "$" in formatted or "," in formatted or "USD" in formatted or formatted.startswith(" ") or formatted.endswith(" ")
        )

    def test_cognitive_rage_clicking(self):
        # Rushed commuter has patience of 1.8s
        # Simulate a 3.5s delay
        did_rage_click, count, intervals = self.cognitive.trigger_rage_click_check(3.5)
        self.assertGreaterEqual(self.cognitive.frustration_score, 10.0)

    def test_audit_reporter(self):
        reporter = AuditReporter("TestApp", "Alex (Rushed Commuter)")
        reporter.add_finding(
            severity="CRITICAL",
            category="Idempotency",
            title="Double Submit Bug",
            description="Created two orders on double click",
            simulated_action="Double clicked submit",
            system_reaction="HTTP 200 twice",
            recommendation="Disable button on click",
        )
        md = reporter.generate_markdown()
        self.assertIn("CRITICAL USABILITY BLOCKERS", md)
        self.assertIn("Double Submit Bug", md)
        json_data = reporter.to_json()
        self.assertIn("TestApp", json_data)

    def test_chat_tester(self):
        tester = ChatTester(self.persona)
        prompts = tester.generate_human_chat_prompts("cancel order")
        self.assertGreaterEqual(len(prompts), 3)

    def test_file_tester(self):
        tester = FileTester(self.persona)
        csv_data = tester.generate_human_csv(include_bom=True)
        self.assertTrue(csv_data.startswith("\ufeff"))
        self.assertIn("Alice Smith", csv_data)

        json_data = tester.generate_human_json()
        self.assertIn("Antigravity Project", json_data)


if __name__ == "__main__":
    unittest.main()
