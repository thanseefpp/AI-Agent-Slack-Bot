import re
from typing import Optional

class AnswerParser:
    def __init__(self, context: str):
        self.context = context
        self.clean_context = self._clean_text(context)

    @staticmethod
    def _clean_text(text: str) -> str:
        return re.sub(r'[^\w\s]', '', text.lower())

    def exact_match(self, question: str) -> Optional[str]:
        clean_question = self._clean_text(question)
        if clean_question in self.clean_context:
            start = self.clean_context.index(clean_question)
            end = self.context.find('.', start + len(question))
            if end == -1:
                return self.context[start:].strip()
            return self.context[start:end + 1].strip()
        return None

    @staticmethod
    def is_low_confidence(answer: str) -> bool:
        low_confidence_phrases = [
            "i'm not sure", "it's unclear", "the context doesn't provide",
            "i don't have enough information", "the text doesn't mention",
            "it's not specified", "i can't determine"
        ]
        return any(phrase in answer.lower() for phrase in low_confidence_phrases)

    @staticmethod
    def parse_api_response(response: dict) -> str:
        return response['choices'][0]['message']['content'].strip()

    def parse_answer(self, question: str, api_response: Optional[dict] = None) -> str:
        exact_match = self.exact_match(question)
        if exact_match:
            return exact_match

        if api_response:
            answer = self.parse_api_response(api_response)
            if self.is_low_confidence(answer) or answer == "Data Not Available":
                return "Data Not Available"
            return answer

        return "Data Not Available"