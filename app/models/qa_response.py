from pydantic import BaseModel
from typing import List, Dict

class QuestionInput(BaseModel):
    questions: List[str]
    slack_channel: str


class QAResponse(BaseModel):
    answers: Dict[str, str]