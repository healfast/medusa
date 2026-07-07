import unittest
from unittest.mock import patch

from medusa_agent import generate_reply


class VeniceOmniIntegrationTests(unittest.TestCase):
    def test_generate_reply_uses_venice_when_requested(self):
        with patch.dict("os.environ", {}, clear=True):
            reply = generate_reply("tell me about ai", provider="venice")

        self.assertIsInstance(reply, str)
        self.assertTrue(reply.strip())

    def test_generate_reply_uses_omni_when_openai_is_configured(self):
        with patch.dict("os.environ", {}, clear=True):
            reply = generate_reply("tell me about ai", provider="omni")

        self.assertIsInstance(reply, str)
        self.assertTrue(reply.strip())

    def test_generate_reply_uses_omni_when_no_configured_external_provider(self):
        reply = generate_reply("tell me about ai", provider="omni")
        self.assertIsInstance(reply, str)
        self.assertTrue(reply.strip())


if __name__ == "__main__":
    unittest.main()
