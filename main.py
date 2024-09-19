from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.v1 import router
from app.utils.api_exceptions import RequestErrorHandler, RequestError
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=[
        "*", # now keeping * for allowing all request but replace this with the React URL
    ],
)

app.include_router(
    router,
    prefix="/v1/",
    tags=["zania_agent"],
)


@app.exception_handler(RequestError)
async def request_error_internal(request, exc):
    reh = RequestErrorHandler(exc=exc)
    return reh.process_message()


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8000,log_level="debug",reload=True)