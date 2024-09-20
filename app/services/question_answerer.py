from openai import OpenAI
from app.utils.error_handlers import OpenAIQueryError
from app.config.env_manager import get_settings
from app.utils.logger import structlog

logger = structlog.get_logger(__name__)
env_settings = get_settings()

class QuestionAnswerer:
    def __init__(self):
        self.client = OpenAI(api_key=env_settings.OPENAI_API_KEY)

    def get_answer(self, question: str, context: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=150,
                temperature=0,
                stop=None,
                n=1,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the given context. If the answer is not explicitly stated in the context, reply with 'Data Not Available'."},
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(e)
            raise OpenAIQueryError(str(e))