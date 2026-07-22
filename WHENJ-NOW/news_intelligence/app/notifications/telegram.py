import os
import requests
from dotenv import load_dotenv

from app.models.article import Article
from app.logging.logger import logger

load_dotenv()


class TelegramNotifier:

    MAX_MESSAGE_LENGTH = 3800

    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.channel_id = os.getenv("TELEGRAM_CHANNEL_ID")

    def _escape_html(self, text: str | None) -> str:
        if not text:
            return ""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def _format_article(self, article: Article) -> str:
        if article.published:
            from datetime import timezone, timedelta
            ist = timezone(timedelta(hours=5, minutes=30))
            published_ist = article.published.astimezone(ist)
            published = published_ist.strftime("%d %b %Y, %I:%M %p")
        else:
            published = "Unknown"
        title = self._escape_html(article.title)
        source = self._escape_html(article.source)
        summary = self._escape_html(article.intelligence_summary)
        link = self._escape_html(article.link)

        return (
            f"📰 <b>{title}</b>\n"
            f"🗞️ {source}  •  📅 {published}\n\n"
            f"{summary}\n\n"
            f"🔗 {link}"
        )

    def send(self, articles: list[Article]):
        if not self.token or not self.channel_id:
            logger.error("Telegram credentials not configured.")
            return

        if not articles:
            logger.info("No articles to send.")
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        separator = "\n\n" + "─" * 40 + "\n\n"

        current_message = ""

        for article in articles:
            block = self._format_article(article)

            # Start a new batch if adding this article exceeds the limit
            if current_message and (
                len(current_message) + len(separator) + len(block)
                > self.MAX_MESSAGE_LENGTH
            ):
                self._send_message(url, current_message)
                current_message = block
            else:
                current_message = (
                    current_message + separator + block
                    if current_message
                    else block
                )

        if current_message:
            self._send_message(url, current_message)

    def _send_message(self, url: str, message: str):
        payload = {
            "chat_id": self.channel_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        response = None
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            logger.info("Telegram message sent successfully.")
        except requests.RequestException as e:
            resp_text = response.text if response is not None else "No response"
            logger.exception(f"Failed to send Telegram message: {e}. Response: {resp_text}")