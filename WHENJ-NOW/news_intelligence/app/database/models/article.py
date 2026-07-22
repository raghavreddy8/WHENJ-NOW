from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database.database import Base


class ArticleModel(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    link = Column(String(1000), unique=True, index=True, nullable=False)
    source = Column(String(255), nullable=False)
    published = Column(DateTime(timezone=True), nullable=True)
    intelligence_summary = Column(Text, nullable=True)
    importance = Column(Integer, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
