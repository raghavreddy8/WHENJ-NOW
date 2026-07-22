from pathlib import Path
from datetime import datetime, timezone
import json


class ArticleStore:

    def __init__(self):

        self.storage_path = (
            Path(__file__).resolve()
            .parent.parent
            / "storage"
            / "today_articles.json"
        )

    def _today(self):
        return datetime.now(timezone.utc).date().isoformat()

    def _load(self):
        default_data = {
            "date": self._today(),
            "articles": []
        }

        if not self.storage_path.exists():
            self._save(default_data)
            return default_data

        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:

                content = f.read().strip()

                if not content:
                    self._save(default_data)
                    return default_data

                return json.loads(content)

        except json.JSONDecodeError:
            self._save(default_data)
            return default_data

    def _save(self, data):

        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

    def add_articles(self, articles):

        data = self._load()

        today = self._today()

        if data["date"] != today:
            data = {
                "date": today,
                "articles": []
            }

        existing_links = {
            article["link"]
            for article in data["articles"]
        }

        for article in articles:

            article_dict = article.model_dump(mode="json")

            if article_dict["link"] not in existing_links:
                data["articles"].insert(
                    0,
                    article_dict
                )

        self._save(data)

    def get_articles(self):
        data = self._load()
            
        if data["date"] != self._today():

            data = {
                "date": self._today(),
                "articles": []
            }

            self._save(data)

        return data["articles"]


article_store = ArticleStore()