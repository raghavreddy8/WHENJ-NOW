import os
import re

import google.genai as genai
from openai import OpenAI
from dotenv import load_dotenv

from app.config.loader import load_config
from app.logging.logger import logger

load_dotenv()


def call_llm(prompt: str) -> str:
    """
    Call the LLM with a plain text prompt.
    Tries Gemini first; falls back to OpenRouter on any error.
    Returns the raw text response.
    """
    try:
        return _call_gemini(prompt)
    except Exception as e:
        logger.warning(f"Gemini failed ({e}). Switching to OpenRouter.")
        return _call_openrouter(prompt)


def _call_gemini(prompt: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    config = load_config()

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(config.llm.gemini.model)
    response = model.generate_content(prompt)
    return response.text


def _call_openrouter(prompt: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    config = load_config()

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )
    response = client.chat.completions.create(
        model=config.llm.openrouter.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


def parse_json_response(response: str) -> str:
    """Strip markdown code fences so the result is valid JSON."""
    response = response.strip()
    if response.startswith("```"):
        response = re.sub(r"^```(?:json)?\s*", "", response, flags=re.IGNORECASE)
        response = re.sub(r"\s*```$", "", response)
    return response.strip()
