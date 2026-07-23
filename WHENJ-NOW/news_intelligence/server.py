import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware

from app.api.articles import router as article_router
from app.scheduler.scheduler import scheduler
from app.database.database import Base, engine
# Import models to ensure they are registered with Base for metadata creation
from app.database.models.article import ArticleModel
from app.database.models.fetch_state import FetchState
from app.database.models.interest import Interest
from main import run_pipeline

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-create any missing tables in Supabase (e.g. the new articles table)
    Base.metadata.create_all(bind=engine)
    
    # Start the background scheduler
    scheduler.start()
    yield
    # Shutdown the background scheduler
    scheduler.shutdown()


app = FastAPI(
    title="WHENJ API",
    lifespan=lifespan
)

origins = [
    "https://whenj-now.vercel.app/",
    "http://127.0.0.1:5500",
    "http://127.0.0.2:5500",
]

frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    origins.append(frontend_url.strip())

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(article_router)


@app.post("/api/trigger-pipeline", status_code=status.HTTP_202_ACCEPTED)
def trigger_pipeline(background_tasks: BackgroundTasks):
    """
    Endpoint for external cron services (like cron-job.org) to trigger the news collection.
    Runs the pipeline asynchronously in background_tasks to avoid HTTP timeout issues on Render.
    """
    background_tasks.add_task(run_pipeline)
    return {"message": "Pipeline execution triggered successfully in the background."}


@app.get("/")
def home():

    return {
        "status": "WHENJ Backend Running"
    }