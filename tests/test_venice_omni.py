import unittest
from unittest.mock import patch

from medusa_agent import generate_reply


class VeniceOmniIntegrationTests(unittest.TestCase):
    @patch("medusa_agent.requests.post")
    def test_generate_reply_uses_venice_when_requested(self, mock_post):
        mock_post.return_value.json.return_value = {"completion": "Venice says hello"}
        mock_post.return_value.raise_for_status.return_value = None

        with patch.dict(
            "os.environ",
            {
                "VENICE_API_KEY": "test-key",
                "VENICE_API_URL": "https://api.venice.ai/v1/completions",
            },
            clear=True,
        ):
            reply = generate_reply("tell me about ai", provider="venice")

        self.assertEqual(reply, "Venice says hello")
        mock_post.assert_called_once()

    @patch("medusa_agent.requests.post")
    def test_generate_reply_uses_omni_when_openai_is_configured(self, mock_post):
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "Omni routed to OpenAI"}}]
        }
        mock_post.return_value.raise_for_status.return_value = None

        with patch.dict(
            "os.environ",
            {
                "OPENAI_API_KEY": "test-key",
                "OPENAI_API_URL": "https://api.openai.com/v1/chat/completions",
                "OPENAI_MODEL": "gpt-4o-mini",
            },
            clear=True,
        ):
            reply = generate_reply("tell me about ai", provider="omni")

        self.assertEqual(reply, "Omni routed to OpenAI")
        mock_post.assert_called_once()

    @patch("medusa_agent.requests.post")
    def test_generate_reply_uses_omni_when_no_configured_external_provider(self, mock_post):
        reply = generate_reply("tell me about ai", provider="omni")
        self.assertIsInstance(reply, str)
        self.assertTrue(reply.strip())
        self.assertGreater(len(reply), 10)
        self.assertNotIn("request failed", reply.lower())
        mock_post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
