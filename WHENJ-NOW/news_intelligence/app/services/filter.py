import re
from app.models.article import Article
from app.logging.logger import logger


def filter_articles(interests, articles: list[Article]) -> list[Article]:
    """
    Keyword filter: keeps articles whose title or RSS description
    contains at least one keyword (using case-insensitive whole-word regex matching).
    """
    if not interests or not articles:
        logger.info("Keyword filter: no interests or articles to process.")
        return []

    # Compile regex patterns for all keywords
    patterns = []
    for interest in interests:
        if interest.keywords:
            for kw in interest.keywords.split(","):
                kw = kw.strip().lower()
                if kw:
                    # Enforce word boundary if the keyword starts or ends with an alphanumeric character
                    pattern_str = ""
                    if kw[0].isalnum():
                        pattern_str += r"\b"
                    pattern_str += re.escape(kw)
                    if kw[-1].isalnum():
                        pattern_str += r"\b"
                    
                    patterns.append(re.compile(pattern_str, re.IGNORECASE))

    if not patterns:
        logger.warning("Keyword filter: no keywords found in interests table.")
        return []

    matched = []
    for article in articles:
        text = f"{article.title} {article.summary}"
        if any(pattern.search(text) for pattern in patterns):
            matched.append(article)

    logger.info(
        f"Keyword filter: {len(matched)}/{len(articles)} articles matched."
    )
    return matched
