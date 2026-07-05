import unittest
from unittest.mock import patch

from medusa_agent import generate_reply


class FableIntegrationTests(unittest.TestCase):
    @patch("medusa_agent.requests.post")
    def test_generate_reply_uses_fable_when_requested(self, mock_post):
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "Fable says hello"}}]
        }
        mock_post.return_value.raise_for_status.return_value = None

        with patch.dict("os.environ", {"FABLE_API_KEY": "test-key", "FABLE_API_URL": "https://api.fable.example/v1"}, clear=True):
            reply = generate_reply("tell me about ai", use_fable=True)

        self.assertEqual(reply, "Fable says hello")
        mock_post.assert_called_once()

    def test_generate_reply_returns_config_message_when_fable_not_configured(self):
        with patch.dict("os.environ", {}, clear=True):
            reply = generate_reply("tell me about ai", use_fable=True)
        self.assertIn("Fable 5 is not configured", reply)


if __name__ == "__main__":
    unittest.main()
