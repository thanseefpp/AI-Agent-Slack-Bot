from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    text: str

class Answer(BaseModel):
    question: str
    answer: str

class ProcessingResult(BaseModel):
    message: str
    results: List[Answer]