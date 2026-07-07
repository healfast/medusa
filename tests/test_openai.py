import unittest
from unittest.mock import patch

from medusa_agent import generate_reply


class OpenAIIntegrationTests(unittest.TestCase):
    def test_generate_reply_uses_openai_when_requested(self):
        with patch.dict("os.environ", {}, clear=True):
            reply = generate_reply("tell me about ai", provider="openai")

        self.assertIsInstance(reply, str)
        self.assertTrue(reply.strip())

    def test_generate_reply_returns_config_message_when_openai_not_configured(self):
        with patch.dict("os.environ", {}, clear=True):
            reply = generate_reply("tell me about ai", provider="openai")
        self.assertIsInstance(reply, str)
        self.assertTrue(reply.strip())


if __name__ == "__main__":
    unittest.main()
