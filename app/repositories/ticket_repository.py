from sqlalchemy.orm import Session

from app.db.models.ticket import Ticket


def create_ticket(
    db: Session,
    title: str,
    description: str,
    creator_id: int
):
    ticket = Ticket(
        title=title,
        description=description,
        creator_id=creator_id
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket