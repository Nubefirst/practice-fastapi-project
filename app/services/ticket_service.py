from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.ticket_repository import (create_ticket,get_user_tickets, get_ticket_by_id, get_tickets_admin, assign_executor, update_ticket_status)
from app.services.audit_log_service import log_action


def create_ticket_service(
    db: Session,
    title: str,
    description: str,
    creator_id: int
):
    ticket = create_ticket(
        db=db,
        title=title,
        description=description,
        creator_id=creator_id
    )

    log_action(
        db=db,
        user_id=creator_id,
        action="CREATE_TICKET",
        entity_type="TICKET",
        entity_id=ticket.id,
        details=f"Created ticket '{ticket.title}'"
    )

    return ticket


def get_user_tickets_service(db: Session, user_id: int):
    return get_user_tickets(db=db, user_id=user_id)


def get_ticket_service(db, ticket_id: int, current_user):
    ticket = get_ticket_by_id(db=db, ticket_id=ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    # проверка доступа
    if ticket.creator_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return ticket


def get_tickets_admin_service(
    db,
    status=None,
    creator_id=None,
    executor_id=None
):
    return get_tickets_admin(
        db=db,
        status=status,
        creator_id=creator_id,
        executor_id=executor_id
    )


def assign_ticket_service(
    db,
    ticket_id: int,
    executor_id: int,
    admin
):
    ticket = get_ticket_by_id(db=db, ticket_id=ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    # защита: только admin уже проверен Depends, но логика остаётся здесь
    updated_ticket = assign_executor(
        db=db,
        ticket=ticket,
        executor_id=executor_id
    )

    log_action(
        db=db,
        user_id=admin.id,
        action="ASSIGN_EXECUTOR",
        entity_type="TICKET",
        entity_id=ticket.id,
        details=f"Assigned executor_id={executor_id}"
    )

    return updated_ticket


def change_status_service(
    db,
    ticket_id: int,
    new_status,
    admin
):
    ticket = get_ticket_by_id(db=db, ticket_id=ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    old_status = ticket.status

    updated_ticket = update_ticket_status(
        db=db,
        ticket=ticket,
        new_status=new_status
    )

    log_action(
        db=db,
        user_id=admin.id,
        action="CHANGE_STATUS",
        entity_type="TICKET",
        entity_id=ticket.id,
        details=f"{old_status} -> {new_status}"
    )

    return updated_ticket


