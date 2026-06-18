from sqlalchemy.orm import Session

from app.repositories.ticket_repository import create_ticket


def create_ticket_service(
    db: Session,
    title: str,
    description: str,
    creator_id: int
):
    return create_ticket(
        db=db,
        title=title,
        description=description,
        creator_id=creator_id
    )