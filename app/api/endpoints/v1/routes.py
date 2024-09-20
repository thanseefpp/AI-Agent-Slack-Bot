from fastapi import APIRouter, UploadFile, File
from http import HTTPStatus
from app.utils.api_exceptions import RequestError
from app.utils.api_error import ErrorCode, ErrorMessage
from app.utils.logger import structlog
from app.models.qa_response import QAResponse, QuestionInput

api_router = APIRouter(tags=["Agent APIs"])
logger = structlog.get_logger(__name__)

@api_router.post('/documents/pdf/qa', response_model=QAResponse)
async def process_pdf_qa(
    user_input: QuestionInput, 
    pdf_file: UploadFile = File(...)
    ):
    try:
        logger.info(user_input)
        return {"message": "Testing"}
    except Exception as e:
        logger.error(e)
        raise RequestError(
            status_code=HTTPStatus.NOT_FOUND,
            error_code=ErrorCode.SOMETHING_WENT_WRONG,
            error_msg=f"{ErrorMessage.REQ_FAILED} :{e}"
            )