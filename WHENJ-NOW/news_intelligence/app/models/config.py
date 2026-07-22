from pydantic import BaseModel


class AppConfig(BaseModel):
    name: str
    environment: str


class ProviderConfig(BaseModel):
    model: str


class LLMConfig(BaseModel):
    gemini: ProviderConfig
    openrouter: ProviderConfig


class SchedulerConfig(BaseModel):
    interval_hours: int


class RSSFeed(BaseModel):
    name: str
    url: str


class Config(BaseModel):
    app: AppConfig
    llm: LLMConfig
    scheduler: SchedulerConfig
    rss_feeds: list[RSSFeed]
