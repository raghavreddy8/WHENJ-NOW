from pydantic import BaseModel

class IntelligenceResponse(BaseModel):
    summary: str
    importance: int
    