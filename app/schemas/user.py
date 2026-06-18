from datetime import datetime

from pydantic import BaseModel
from pydantic import EmailStr

from app.db.models.enums import UserRole


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True