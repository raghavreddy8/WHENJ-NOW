from datetime import datetime, timedelta, timezone
import email.utils
import feedparser

from app.logging.logger import logger
from app.models.article import Article
from app.config.loader import load_config


class RSSCollector:

    def __init__(self):
        self.feeds = load_config().rss_feeds

    def _parse_rss_date(self, date_str: str | None) -> datetime | None:
        if not date_str:
            return None
        try:
            cleaned_str = date_str.strip()
            # If the string ends with 'IST' or contains 'IST', replace with '+0530'
            if cleaned_str.endswith(" IST"):
                cleaned_str = cleaned_str[:-4] + " +0530"
            elif " IST" in cleaned_str:
                cleaned_str = cleaned_str.replace(" IST", " +0530")

            dt = email.utils.parsedate_to_datetime(cleaned_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except Exception:
            return None

    def collect(self, last_checked: datetime | None = None) -> list[Article]:
        """
        Fetch all RSS feeds and return articles published after last_checked.
        Enforces a maximum lookback window of 24 hours.
        """
        
        max_lookback = datetime.now(timezone.utc) - timedelta(hours=24)
        if last_checked is None or last_checked < max_lookback:
            last_checked = max_lookback

        articles = []
        seen_links: set[str] = set()

        for feed in self.feeds:
            try:
                parsed = feedparser.parse(feed.url)

                for entry in parsed.entries:
                    # Deduplicate by link
                    link = getattr(entry, "link", None)
                    if not link or link in seen_links:
                        continue

                    # Extract publish timestamp
                    pub_str = getattr(entry, "published", None) or getattr(entry, "updated", None)
                    article_time = self._parse_rss_date(pub_str)

                    if not article_time:
                        if hasattr(entry, "published_parsed") and entry.published_parsed:
                            article_time = datetime(
                                *entry.published_parsed[:6], tzinfo=timezone.utc
                            )
                        elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                            article_time = datetime(
                                *entry.updated_parsed[:6], tzinfo=timezone.utc
                            )

                    # Skip undated or already-seen articles
                    if not article_time or article_time <= last_checked:
                        continue

                    seen_links.add(link)
                    articles.append(
                        Article(
                            title=getattr(entry, "title", ""),
                            summary=getattr(entry, "summary", ""),
                            link=link,
                            source=feed.name,
                            published=article_time,
                        )
                    )

            except Exception:
                logger.exception(f"Failed to parse RSS feed: {feed.name}")
                continue

        logger.info(f"RSS collector: {len(articles)} new articles found.")
        return articles