import unittest

from medusa_agent import generate_reply


class HermesJailbreakTests(unittest.TestCase):
    def test_default_mode_is_hermes_godmode(self):
        reply = generate_reply("hello there")
        self.assertIsInstance(reply, str)
        self.assertTrue(reply.strip())
        self.assertTrue(reply.startswith("[Hermes - direct]") or "hermes" in reply.lower())

    def test_local_jailbreak_mode_planning(self):
        reply = generate_reply("plan a blog backend", provider="local", jailbreak=True)
        self.assertIsInstance(reply, str)
        self.assertTrue(reply.strip())
        self.assertTrue(reply.startswith("[Hermes - direct]") or "hermes" in reply.lower())

    def test_local_jailbreak_mode_coding(self):
        reply = generate_reply("write a login endpoint", provider="local", jailbreak=True)
        self.assertIsInstance(reply, str)
        self.assertTrue(reply.strip())
        self.assertTrue(reply.startswith("[Hermes - direct]") or "hermes" in reply.lower())

    def test_claude_code_jailbreak_mode_falls_back(self):
        reply = generate_reply("write a function", provider="claude_code", jailbreak=True)
        self.assertIsInstance(reply, str)
        self.assertTrue(reply.strip())


if __name__ == "__main__":
    unittest.main()
