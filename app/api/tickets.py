from fastapi import APIRouter
from fastapi import Depends
from typing import List
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user

from app.schemas.ticket import TicketCreate, TicketResponse

from app.services.ticket_service import create_ticket_service, get_user_tickets_service, get_ticket_service

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

@router.post("/", response_model=TicketResponse)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_ticket_service(
        db=db,
        title=ticket_data.title,
        description=ticket_data.description,
        creator_id=current_user.id
    )


@router.get("/my", response_model=List[TicketResponse])
def get_my_tickets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_user_tickets_service(
        db=db,
        user_id=current_user.id
    )


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_ticket_service(
        db=db,
        ticket_id=ticket_id,
        current_user=current_user
    )