from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user

from app.schemas.ticket import TicketCreate, TicketResponse

from app.services.ticket_service import create_ticket_service


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