from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from app.dependencies.auth import get_current_admin
from app.dependencies.database import get_db

from app.schemas.ticket import TicketResponse
from app.services.ticket_service import get_tickets_admin_service, assign_ticket_service, change_status_service
from app.db.models.enums import TicketStatus

from app.db.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

class AssignRequest(BaseModel):
    executor_id: int


class StatusUpdateRequest(BaseModel):
    status: TicketStatus


@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(User).all()


@router.get("/tickets", response_model=List[TicketResponse])
def get_all_tickets(
    status: TicketStatus | None = None,
    creator_id: int | None = None,
    executor_id: int | None = None,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return get_tickets_admin_service(
        db=db,
        status=status,
        creator_id=creator_id,
        executor_id=executor_id
    )


@router.patch("/tickets/{ticket_id}/assign", response_model=TicketResponse)
def assign_ticket(
    ticket_id: int,
    data: AssignRequest,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return assign_ticket_service(
        db=db,
        ticket_id=ticket_id,
        executor_id=data.executor_id,
        admin=admin
    )


@router.patch("/tickets/{ticket_id}/status", response_model=TicketResponse)
def change_status(
    ticket_id: int,
    data: StatusUpdateRequest,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return change_status_service(
        db=db,
        ticket_id=ticket_id,
        new_status=data.status,
        admin=admin
    )