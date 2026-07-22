from datetime import datetime
from pydantic import BaseModel


class Article(BaseModel):
    title: str
    summary: str       # RSS feed description/summary
    link: str
    source: str
    published: datetime | None = None

    # Filled after summarization
    intelligence_summary: str | None = None
    importance: int | None = None