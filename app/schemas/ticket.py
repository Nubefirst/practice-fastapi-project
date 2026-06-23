from pydantic import BaseModel
from datetime import datetime

from app.db.models.enums import TicketStatus


class TicketCreate(BaseModel):
    title: str
    description: str


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TicketStatus

    creator_id: int
    executor_id: int | None

    created_at: datetime

    model_config = {
        "from_attributes": True
    }