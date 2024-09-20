from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.v1 import routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"] # now keeping * for allowing all request but replace this with the React URL
)

app.include_router(
    routes.api_router,
    prefix="/api/v1",
    tags=["zania_agent"],
)

@app.get("/")
async def root():
    return {"message": "AI Agent Started"}