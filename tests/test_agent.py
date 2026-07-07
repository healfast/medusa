import unittest

from medusa_agent import generate_reply


class MedusaAgentTests(unittest.TestCase):
    def test_generate_reply_returns_text(self):
        reply = generate_reply("hello")
        self.assertIsInstance(reply, str)
        self.assertTrue(reply.strip())

    def test_generate_reply_can_plan_a_project(self):
        reply = generate_reply("build a todo app")
        self.assertIn("plan", reply.lower())
        self.assertIn("milestone", reply.lower())

    def test_generate_reply_uses_conversation_history(self):
        history = [
            {"role": "user", "content": "I want to build a blog"},
            {"role": "assistant", "content": "I can help with that."},
        ]
        reply = generate_reply("continue the plan", history=history)
        self.assertIn("plan", reply.lower())


if __name__ == "__main__":
    unittest.main()
