from app.database.database import SessionLocal
from app.database.models.interest import Interest


class InterestRepository:

    def get_all(self) -> list[Interest]:
        """Return all Interest ORM rows (interest_name + keywords)."""
        db = SessionLocal()
        try:
            return db.query(Interest).all()
        finally:
            db.close()