import unittest
from unittest.mock import patch

from medusa_agent import generate_reply


class HuggingFaceIntegrationTests(unittest.TestCase):
    @patch("medusa_agent.requests.post")
    def test_generate_reply_uses_huggingface_when_requested(self, mock_post):
        mock_post.return_value.json.return_value = {"generated_text": "Hugging Face says hello"}
        mock_post.return_value.raise_for_status.return_value = None

        with patch.dict(
            "os.environ",
            {
                "HUGGINGFACE_API_TOKEN": "test-token",
                "HUGGINGFACE_MODEL": "gpt2",
                "HUGGINGFACE_API_URL": "https://api-inference.huggingface.co/models",
            },
            clear=True,
        ):
            reply = generate_reply("tell me about ai", provider="huggingface")

        self.assertEqual(reply, "Hugging Face says hello")
        mock_post.assert_called_once()

    def test_generate_reply_returns_config_message_when_huggingface_not_configured(self):
        with patch.dict("os.environ", {}, clear=True):
            reply = generate_reply("tell me about ai", provider="huggingface")
        self.assertIn("Hugging Face is not configured", reply)


if __name__ == "__main__":
    unittest.main()
