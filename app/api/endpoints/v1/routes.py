from fastapi import APIRouter
from http import HTTPStatus
from app.utils.api_exceptions import RequestError
from app.utils.api_error import ErrorCode, ErrorMessage


api_router = APIRouter(tags=["Agent APIs"])


@api_router.post('/generate_response/')
async def generate_agent_response():
    try:
        data = {"Success ":"Test completed"}
        return data
    except Exception as e:
        raise RequestError(
            status_code=HTTPStatus.NOT_FOUND,
            error_code=ErrorCode.INCORRECT_USER_ID,
            error_msg=f"{ErrorMessage.REQ_FAILED} :{e}"
            )