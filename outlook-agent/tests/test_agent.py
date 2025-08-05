import unittest
from unittest.mock import patch, MagicMock
import sys
sys.modules["exchangelib"] = MagicMock()
sys.modules["langchain"] = MagicMock()
sys.modules["dotenv"] = MagicMock()

from outlook_agent import agent

class TestAgent(unittest.TestCase):
    @patch("outlook_agent.agent.connect_to_outlook")
    def test_read_latest_email_no_unread(self, mock_connect):
        mock_account = MagicMock()
        mock_account.inbox.filter.return_value.order_by.return_value = []
        mock_connect.return_value = mock_account
        result = agent.read_latest_email("")
        self.assertEqual(result, "No unread emails.")

    @patch("outlook_agent.agent.connect_to_outlook")
    @patch("builtins.input", return_value="n")
    def test_confirm_and_send_reply_not_sent(self, mock_input, mock_connect):
        mock_account = MagicMock()
        mock_msg = MagicMock()
        mock_account.inbox.filter.return_value.order_by.return_value = [mock_msg]
        mock_connect.return_value = mock_account
        result = agent.confirm_and_send_reply("Test reply")
        self.assertEqual(result, "Reply not sent.")

    @patch("outlook_agent.agent.connect_to_outlook")
    @patch("builtins.input", return_value="y")
    def test_confirm_and_send_reply_sent(self, mock_input, mock_connect):
        mock_account = MagicMock()
        mock_msg = MagicMock()
        mock_reply = MagicMock()
        mock_msg.reply.return_value = mock_reply
        mock_account.inbox.filter.return_value.order_by.return_value = [mock_msg]
        mock_connect.return_value = mock_account
        result = agent.confirm_and_send_reply("Test reply")
        self.assertEqual(result, "Reply sent.")

if __name__ == "__main__":
    unittest.main()
