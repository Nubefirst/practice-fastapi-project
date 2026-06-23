from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.models.ticket import Ticket
from app.db.models.enums import TicketStatus


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


def get_user_tickets(
    db: Session,
    user_id: int
):
    return db.query(Ticket).filter(
        Ticket.creator_id == user_id
    ).all()

def get_ticket_by_id(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


def get_tickets_admin(
    db: Session,
    status: TicketStatus | None = None,
    creator_id: int | None = None,
    executor_id: int | None = None
):
    query = db.query(Ticket)

    filters = []

    if status:
        filters.append(Ticket.status == status)

    if creator_id:
        filters.append(Ticket.creator_id == creator_id)

    if executor_id:
        filters.append(Ticket.executor_id == executor_id)

    if filters:
        query = query.filter(and_(*filters))

    return query.all()


def assign_executor(
    db: Session,
    ticket: Ticket,
    executor_id: int
):
    ticket.executor_id = executor_id
    db.commit()
    db.refresh(ticket)
    return ticket

def update_ticket_status(
    db: Session,
    ticket: Ticket,
    new_status: TicketStatus
):
    ticket.status = new_status
    db.commit()
    db.refresh(ticket)
    return ticket
