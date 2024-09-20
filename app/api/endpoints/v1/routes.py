from fastapi import APIRouter, UploadFile, File, Form
from app.utils.logger import structlog
from app.models.qa_response import Question, ProcessingResult, Answer
from app.services.document_processor import DocumentProcessor
from app.services.question_answerer import QuestionAnswerer
import json

api_router = APIRouter(tags=["Agent APIs"])
logger = structlog.get_logger(__name__)

@api_router.post('/documents/qa', response_model=ProcessingResult)
async def process_pdf_qa(questions: str = Form(...), pdf_file: UploadFile = File(...)) -> ProcessingResult:
    questions_list = json.loads(questions)
    questions_objects = [Question(**q) for q in questions_list]

    doc_processor = DocumentProcessor()
    question_answerer = QuestionAnswerer()

    vector_db = doc_processor.process_pdf(pdf_file)

    results = []
    for question in questions_objects:
        context = doc_processor.get_relevant_context(vector_db, question.text)
        answer = question_answerer.get_answer(question.text, context)
        results.append(Answer(question=question.text, answer=answer))
    
    return ProcessingResult(
        message="Here is your answer",
        results=results
    )