from sqlalchemy import Column, Integer, String, Text

from app.database.database import Base


class Interest(Base):

    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)

    interest_name = Column(
        String(255),
        unique=True,
        nullable=False
    )

    # Comma-separated keywords, e.g. "AI, LLM, GPT, neural network"
    keywords = Column(
        Text,
        nullable=False
    )