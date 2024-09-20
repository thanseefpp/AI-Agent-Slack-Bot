from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.v1 import routes
from app.utils.api_exceptions import RequestErrorHandler, RequestError

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"] # now keeping * for allowing all request but replace this with the React URL
)

app.include_router(
    routes,
    prefix="/v1/",
    tags=["zania_agent"],
)


@app.exception_handler(RequestError)
async def request_error_internal(request, exc):
    reh = RequestErrorHandler(exc=exc)
    return reh.process_message()


@app.get("/")
async def root():
    return {"message": "AI Agent Started"}