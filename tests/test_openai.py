import unittest
from unittest.mock import patch

from medusa_agent import generate_reply


class OpenAIIntegrationTests(unittest.TestCase):
    @patch("medusa_agent.requests.post")
    def test_generate_reply_uses_openai_when_requested(self, mock_post):
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "OpenAI says hello"}}]
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
            reply = generate_reply("tell me about ai", provider="openai")

        self.assertEqual(reply, "OpenAI says hello")
        mock_post.assert_called_once()

    def test_generate_reply_returns_config_message_when_openai_not_configured(self):
        with patch.dict("os.environ", {}, clear=True):
            reply = generate_reply("tell me about ai", provider="openai")
        self.assertIn("OpenAI is not configured", reply)


if __name__ == "__main__":
    unittest.main()
