import os
from slack import WebClient
from slack.errors import SlackApiError
from app.utils.error_handlers import SlackPostingError
from app.config.env_manager import get_settings
from app.utils.logger import structlog

logger = structlog.get_logger(__name__)
env_settings = get_settings()

class SlackNotifier:
    def __init__(self):
        self.client = WebClient(token=env_settings.SLACK_API_TOKEN)

    def push_notification(self, message: str):
        try:
            response = self.client.chat_postMessage(
                channel='#ai-bot-response',
                text=message)
            assert response["message"]["text"] == message
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            logger.error(f"Got an error: {e.response['error']}")
            raise SlackPostingError(str(e))