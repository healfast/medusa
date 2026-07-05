import unittest

from medusa_agent import generate_reply


class HermesJailbreakTests(unittest.TestCase):
    def test_local_jailbreak_mode_planning(self):
        reply = generate_reply("plan a blog backend", provider="local", jailbreak=True)
        self.assertIn("Hermes jailbreak mode", reply)
        self.assertIn("direct plan", reply.lower())

    def test_local_jailbreak_mode_coding(self):
        reply = generate_reply("write a login endpoint", provider="local", jailbreak=True)
        self.assertIn("Hermes jailbreak mode", reply)
        self.assertIn("direct coding guidance", reply.lower())

    def test_claude_code_jailbreak_mode_falls_back(self):
        reply = generate_reply("write a function", provider="claude_code", jailbreak=True)
        self.assertTrue(reply.startswith("Claude Code is not configured") or "Claude Code request failed" in reply)


if __name__ == "__main__":
    unittest.main()
