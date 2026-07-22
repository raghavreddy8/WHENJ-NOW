from app.models.article import Article
from app.models.intelligence_response import IntelligenceResponse
from app.prompts.article_summary_prompt import SYSTEM_PROMPT
from app.services.llm import call_llm, parse_json_response
from app.logging.logger import logger


def summarize(article: Article) -> Article:
    """
    Call the LLM to produce a concise summary and importance score
    for a given article, using its title + RSS description as input.
    Mutates and returns the same article with intelligence_summary
    and importance filled in.
    """
    prompt = f"""
{SYSTEM_PROMPT}

Title:
{article.title}

Published:
{article.published}

Source:
{article.source}

Description:
{article.summary}
"""

    raw = call_llm(prompt)
    clean = parse_json_response(raw)

    intelligence = IntelligenceResponse.model_validate_json(clean)

    article.intelligence_summary = intelligence.summary
    article.importance = intelligence.importance

    logger.info(f"Summarized: {article.title}")
    return article
