import aiohttp
import asyncio
import tiktoken
from typing import List, Tuple, Dict
from langchain_community.vectorstores import FAISS
from app.utils.error_handlers import OpenAIQueryError
from app.config.env_manager import get_settings
from app.utils.logger import structlog
from app.services.answer_parser import AnswerParser
from app.services.document_processor import DocumentProcessor
from app.models.qa_response import Answer, Question

logger = structlog.get_logger(__name__)
env_settings = get_settings()

class QuestionAnswerer:
    def __init__(self):
        self.api_key = env_settings.OPENAI_API_KEY
        self.session = None
        self.encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0
        
    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))

    async def get_api_response(self, question: str, context: str) -> dict:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the given context. If the answer is not explicitly stated in the context or if you're not confident in your answer, reply with 'Data Not Available'"},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]
        
        input_tokens = sum(self.count_tokens(m['content']) for m in messages)
        self.input_tokens += input_tokens
        self.total_tokens += input_tokens

        async with self.session.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": "gpt-4o-mini",
                "messages": messages,
                "max_tokens": 150,
                "n": 1,
                "stop": None,
                "temperature": 0,
            }
        ) as response:
            result = await response.json()
            output_tokens = self.count_tokens(result['choices'][0]['message']['content'])
            self.output_tokens += output_tokens
            self.total_tokens += output_tokens
            return result

    async def process_question(self, question: str, context: str) -> str:
        parser = AnswerParser(context)
        exact_match = parser.exact_match(question)
        if exact_match:
            return exact_match
        api_response = await self.get_api_response(question, context)
        return parser.parse_answer(question, api_response)

    async def get_answers(self, questions_and_contexts: List[Tuple[str, str]]) -> List[str]:
        try:
            _ = await self.get_session()
            tasks = [self.process_question(question, context) for question, context in questions_and_contexts]
            answers = await asyncio.gather(*tasks)
            return answers
        except Exception as e:
            logger.error(str(e))
            raise OpenAIQueryError(str(e))
        
    async def close(self):
        if self.session:
            await self.session.close()

    def get_token_usage(self) -> Dict[str, float]:
        return {
            "total_tokens": self.total_tokens,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "estimated_cost": (self.input_tokens / 1000) * 0.000075  # $0.000075 per 1K input tokens(Take from OpenAI official pricing)
        }


async def process_questions(doc_processor: DocumentProcessor, question_answerer: QuestionAnswerer, vector_db: FAISS, questions: List[Question]) -> Tuple[List[Answer], Dict[str, float]]:
    questions_and_contexts = [(q.text, doc_processor.get_relevant_context(vector_db, q.text)) for q in questions]
    answers = await question_answerer.get_answers(questions_and_contexts)
    results = [Answer(question=q.text, answer=a) for q, a in zip(questions, answers)]
    token_usage = question_answerer.get_token_usage()
    return results, token_usage