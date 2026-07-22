from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.articles import router as article_router

app = FastAPI(
    title="WHENJ API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://127.0.0.2:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(article_router)


@app.get("/")
def home():

    return {
        "status": "WHENJ Backend Running"
    }