from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
import json
from app.utils.logger import structlog
from app.models.qa_response import Question, ProcessedResult
from app.services.document_processor import DocumentProcessor, get_loaded_document
from app.services.question_answerer import QuestionAnswerer, process_questions
from app.services.slack_notifier import SlackNotifier, format_slack_message


api_router = APIRouter(tags=["Agent APIs"])
logger = structlog.get_logger(__name__)

@api_router.post('/documents/qa', response_model=ProcessedResult)
async def process_pdf_qa(
    background_tasks: BackgroundTasks,
    questions: str = Form(...),
    pdf_file: UploadFile = File(...),
) -> ProcessedResult:
    questions_list = json.loads(questions)
    questions_objects = [Question(**q) for q in questions_list]

    doc_processor = DocumentProcessor()
    question_answerer = QuestionAnswerer()
    slack_notifier = SlackNotifier()

    vector_db = await get_loaded_document(pdf_file)
    results, token_usage = await process_questions(doc_processor, question_answerer, vector_db, questions_objects)
    formatted_response : str = format_slack_message(results,token_usage)
    background_tasks.add_task(slack_notifier.push_notification, formatted_response)
    return ProcessedResult(
        message="Here is the answer to your questions",
        results=results
    )