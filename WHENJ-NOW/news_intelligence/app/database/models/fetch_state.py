from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime

from app.database.database import Base


class FetchState(Base):

    __tablename__ = "fetch_state"

    id = Column(
        Integer,
        primary_key=True
    )

    last_checked = Column(
        DateTime(timezone=True),
        nullable=False
    )