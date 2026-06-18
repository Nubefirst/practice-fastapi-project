from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.user import UserCreate
from app.schemas.user import UserResponse

from app.schemas.auth import LoginRequest
from app.schemas.auth import TokenResponse

from app.services.auth_service import register_user
from app.services.auth_service import login_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user(
        db=db,
        username=user.username,
        email=user.email,
        password=user.password
    )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    return login_user(
        db=db,
        email=credentials.email,
        password=credentials.password
    )