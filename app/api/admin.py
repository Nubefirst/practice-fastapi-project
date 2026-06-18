from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_admin
from app.dependencies.database import get_db

from app.db.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(User).all()