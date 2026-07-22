from datetime import datetime,timezone

from fastapi import APIRouter

from app.services.article_store import article_store

router = APIRouter(
    prefix="/api/articles",
    tags=["Articles"]
)

@router.get("/today")
def get_today_articles():

    articles = article_store.get_articles()

    return {
        "count": len(articles),
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "articles": articles
    }