from datetime import datetime, timezone

from app.collectors.rss_collector import RSSCollector
from app.services.filter import filter_articles
from app.services.summarizer import summarize
from app.notifications.telegram import TelegramNotifier
from app.logging.logger import logger
from app.database.interest_repository import InterestRepository
from app.database.fetch_state_repository import FetchStateRepository
from app.services.article_store import article_store



def run_pipeline():
    logger.info("Pipeline started.")
    pipeline_started_at = datetime.now(timezone.utc)

    fetch_repo = FetchStateRepository()
    interest_repo = InterestRepository()

    try:
        interests = interest_repo.get_all()
        last_checked = fetch_repo.get_last_checked()

        # 1. Collect articles published since last run
        articles = RSSCollector().collect(last_checked)

        if not articles:
            logger.info("No new articles since last check.")
            fetch_repo.update_last_checked(pipeline_started_at)
            return

        # 2. Filter by keyword match against user interests
        filtered = filter_articles(interests, articles)

        if not filtered:
            logger.info("No articles matched user interests.")
            fetch_repo.update_last_checked(pipeline_started_at)
            return

        # Sort filtered articles by published date (newest first) and limit to top 10
        filtered.sort(
            key=lambda a: a.published if a.published is not None else datetime.min.replace(tzinfo=timezone.utc),
            reverse=True
        )
        filtered = filtered[:10]
        logger.info(f"Limiting to the {len(filtered)} newest matching articles for summarization.")

        # 3. Summarize each matched article
        summarized = []
        for article in filtered:
            try:
                summarized.append(summarize(article))
            except Exception:
                logger.exception(f"Failed to summarize: {article.title}")
                continue

        # 4. Send to Telegram
        if summarized:
            TelegramNotifier().send(summarized)
            article_store.add_articles(summarized)

        # 5. Save the timestamp of this run
        fetch_repo.update_last_checked(pipeline_started_at)
        logger.info(f"Pipeline done. {len(summarized)} articles sent.")

    except Exception:
        logger.exception("Pipeline execution failed.")


if __name__ == "__main__":
    try:
        run_pipeline()
    except KeyboardInterrupt:
        logger.info("Pipeline execution interrupted by user.")