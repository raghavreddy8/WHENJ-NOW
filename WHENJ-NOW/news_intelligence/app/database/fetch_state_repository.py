from datetime import datetime,timedelta,timezone

from app.database.database import SessionLocal
from app.database.models.fetch_state import FetchState


class FetchStateRepository:

    def get_last_checked(self):

        db = SessionLocal()

        try:
            state = (
                db.query(FetchState)
                .filter(FetchState.id == 1)
                .first()
            )

            if state is None:
                return (
                    datetime.now(timezone.utc)
                    - timedelta(hours=1)
                )

            return state.last_checked

        finally:
            db.close()

    def update_last_checked(self,
                            last_checked: datetime):

        db = SessionLocal()

        try:

            state = (
                db.query(FetchState)
                .filter(FetchState.id == 1)
                .first()
            )

            if state is None:

                state = FetchState(
                    id=1,
                    last_checked=last_checked
                )

                db.add(state)

            else:

                state.last_checked = last_checked

            db.commit()

        finally:

            db.close()