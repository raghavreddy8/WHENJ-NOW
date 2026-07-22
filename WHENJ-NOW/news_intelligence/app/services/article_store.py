from datetime import datetime, timezone
from app.database.database import SessionLocal
from app.database.models.article import ArticleModel


class ArticleStore:

    def add_articles(self, articles):
        db = SessionLocal()
        try:
            # Query existing links to avoid inserting duplicate entries
            existing_links = {
                link_tuple[0] for link_tuple in db.query(ArticleModel.link).all()
            }

            for article in articles:
                if article.link not in existing_links:
                    db_article = ArticleModel(
                        title=article.title,
                        summary=article.summary,
                        link=article.link,
                        source=article.source,
                        published=article.published,
                        intelligence_summary=article.intelligence_summary,
                        importance=article.importance
                    )
                    db.add(db_article)
            db.commit()
        finally:
            db.close()

    def get_articles(self):
        db = SessionLocal()
        try:
            # Get start of today (UTC)
            today_start = datetime.now(timezone.utc).replace(
                hour=0, minute=0, second=0, microsecond=0
            )

            # Retrieve articles created/processed today (UTC), sorted by publication date descending
            articles = (
                db.query(ArticleModel)
                .filter(ArticleModel.created_at >= today_start)
                .order_by(ArticleModel.published.desc())
                .all()
            )

            return [
                {
                    "title": a.title,
                    "summary": a.summary,
                    "link": a.link,
                    "source": a.source,
                    "published": a.published.isoformat() if a.published else None,
                    "intelligence_summary": a.intelligence_summary,
                    "importance": a.importance
                }
                for a in articles
            ]
        finally:
            db.close()


article_store = ArticleStore()