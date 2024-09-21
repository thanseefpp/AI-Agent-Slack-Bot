from fastapi import HTTPException

class PDFProcessingError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=f"Error processing PDF: {detail}")

class OpenAIQueryError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=f"Error querying OpenAI: {detail}")

class SlackPostingError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=f"Error posting to Slack: {detail}")

class DataHanlderError(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)