import unittest
from unittest.mock import patch

from medusa_agent import generate_reply


class ClaudeCodeIntegrationTests(unittest.TestCase):
    @patch("medusa_agent.requests.post")
    def test_generate_reply_uses_claude_code_when_requested(self, mock_post):
        mock_post.return_value.json.return_value = {"completion": "Claude Code responds."}
        mock_post.return_value.raise_for_status.return_value = None

        with patch.dict(
            "os.environ",
            {
                "CLAUDE_API_URL": "https://api.anthropic.com/v1/complete",
                "CLAUDE_API_KEY": "test-key",
            },
            clear=True,
        ):
            reply = generate_reply("tell me about ai", provider="claude_code")

        self.assertEqual(reply, "Claude Code responds.")
        mock_post.assert_called_once()

    def test_generate_reply_returns_config_message_when_claude_not_configured(self):
        with patch.dict("os.environ", {}, clear=True):
            reply = generate_reply("tell me about ai", provider="claude_code")
        self.assertIn("Claude Code is not configured", reply)


if __name__ == "__main__":
    unittest.main()
