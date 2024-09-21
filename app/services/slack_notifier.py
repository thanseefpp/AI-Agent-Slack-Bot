import aiohttp
import json
from slack_sdk.errors import SlackApiError
from app.utils.error_handlers import SlackPostingError
from app.config.env_manager import get_settings
from app.utils.logger import structlog
from app.models.qa_response import Answer
from typing import List

logger = structlog.get_logger(__name__)
env_settings = get_settings()

class SlackNotifier:
    def __init__(self):
        self.token = env_settings.SLACK_API_TOKEN
        self.channel = env_settings.SLACK_CHANNEL
        self.session = None
    
    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def push_notification(self, message: str) -> None:
        try:
            session = await self.get_session()
            async with session.post(
                "https://slack.com/api/chat.postMessage",
                headers={"Authorization": f"Bearer {self.token}"},
                json={
                    "channel": self.channel,
                    "text": message
                }
            ) as response:
                if response.status != 200:
                    raise SlackPostingError(f"Failed to post message: {await response.text()}")
        except SlackApiError as e:
            logger.error(str(e))
            raise SlackPostingError(str(e))
        
    async def close(self):
        if self.session:
            await self.session.close()


def format_slack_message(results: List[Answer]) -> str:
    output = json.dumps([result.dict() for result in results], indent=2)
    return f"AI Generated Response:\n```\n{output}\n```"