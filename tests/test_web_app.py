import unittest

from app import create_app


class MedusaWebAppTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_home_page_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Medusa", response.data)

    def test_chat_api_returns_reply(self):
        response = self.client.post(
            "/api/chat",
            json={"message": "build a todo app", "provider": "local"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("reply", response.get_json())
        self.assertTrue(response.get_json()["reply"].strip())

    def test_chat_api_uses_provider_parameter(self):
        response = self.client.post(
            "/api/chat",
            json={"message": "build a todo app", "provider": "claude_code"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("reply", response.get_json())
        self.assertTrue(response.get_json()["reply"].strip())


if __name__ == "__main__":
    unittest.main()
