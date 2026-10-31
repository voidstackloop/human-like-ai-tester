"""Conversational, Chatbot & Voice Assistant Tester - Human Simulation."""

import random
from typing import Dict, List, Optional
from ..personas import Persona
from ..typo_engine import TypoEngine
from ..reporter import AuditReporter

HUMAN_CONVERSATIONAL_PATTERNS = [
    {
        "id": "vague_complaint",
        "description": "User provides almost zero context expecting AI/agent to guess.",
        "prompts": [
            "It doesn't work.",
            "Why is my account broken?",
            "Fix this please.",
            "I can't see the thing.",
        ],
    },
    {
        "id": "mid_sentence_reversal",
        "description": "User changes their mind midway through the message.",
        "prompts": [
            "Please cancel my order #9821. Wait actually no, don't cancel it! Just update the shipping address.",
            "Delete my profile... actually wait, can I just export my data first?",
            "Transfer $500 to savings, no wait make that $250.",
        ],
    },
    {
        "id": "premature_enter_key",
        "description": "User accidentally pressed Enter before finishing the question.",
        "prompts": [
            "Hi, I was wondering how to",
            "When I click on the settings tab it",
            "Can you tell me if",
        ],
    },
    {
        "id": "slang_and_abbreviations",
        "description": "User types informal shorthand and internet slang.",
        "prompts": [
            "yo can u plz lmk why my sub aint working thx",
            "idk where 2 find my receipt rn, halp",
            "r u guys srsly charging me twice wtf",
        ],
    },
    {
        "id": "rambling_emotional_stream",
        "description": "User tells a long emotional story with the actual request buried.",
        "prompts": [
            "So my morning started terrible because my car broke down and then my boss yelled at me and when I finally sat down to drink coffee my laptop died and now I'm trying to reset my password but I don't remember my email. Can you reset it for phone 555-0192?",
        ],
    },
    {
        "id": "ambiguous_pronoun_reference",
        "description": "User refers to multiple entities using ambiguous pronouns (it, they, that).",
        "prompts": [
            "I checked the file and the database, but it had an error so I removed it. Can you restore that?",
        ],
    },
]


class ChatTester:
    """Generates authentic human conversational behaviors for testing Chatbots and Voice AIs."""

    def __init__(self, persona: Persona, reporter: Optional[AuditReporter] = None):
        self.persona = persona
        self.typo_engine = TypoEngine()
        self.reporter = reporter or AuditReporter("Conversational Interface", persona.name)

    def generate_human_chat_prompts(self, core_task: str) -> List[Dict[str, str]]:
        """Turn a clean intent into diverse, realistic human conversational inputs."""
        results = []
        for pattern in HUMAN_CONVERSATIONAL_PATTERNS:
            base_prompt = random.choice(pattern["prompts"])
            # Apply persona typo rate
            if self.persona.typo_rate > 0.15:
                humanized = self.typo_engine.introduce_typos(base_prompt, error_rate=self.persona.typo_rate)
            else:
                humanized = base_prompt

            results.append({
                "pattern_id": pattern["id"],
                "description": pattern["description"],
                "human_prompt": humanized,
            })
        return results

    def evaluate_assistant_response(self, prompt_pattern_id: str, assistant_reply: str) -> Dict:
        """Evaluate if chatbot responded gracefully to human ambiguity or broke down."""
        reply_lower = assistant_reply.lower()

        # Check for unhelpful canned failure
        canned_failures = ["i do not understand", "system error", "invalid command", "an error occurred"]
        is_canned = any(cf in reply_lower for cf in canned_failures)

        if is_canned:
            self.reporter.add_finding(
                severity="FRICTION",
                category="Conversational Resilience",
                title=f"Chatbot Broke Down on Human Pattern '{prompt_pattern_id}'",
                description="Chatbot responded with a rigid canned error rather than asking clarifying questions.",
                simulated_action=f"Prompt pattern: {prompt_pattern_id}",
                system_reaction=assistant_reply[:150],
                recommendation="Train/prompt agent to ask gentle clarifying questions when input is ambiguous or incomplete.",
            )

        return {
            "pattern_id": prompt_pattern_id,
            "handled_gracefully": not is_canned,
            "response_preview": assistant_reply[:200],
        }
