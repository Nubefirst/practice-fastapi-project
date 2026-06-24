from pydantic import BaseModel
from datetime import datetime


class AuditLogResponse(BaseModel):
    id: int
    user_id: int

    action: str
    entity_type: str
    entity_id: int

    details: str | None

    created_at: datetime

    model_config = {
        "from_attributes": True
    }