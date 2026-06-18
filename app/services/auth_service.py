from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.core.security import hash_password
from app.core.security import verify_password
from app.repositories.user_repository import create_user
from app.repositories.user_repository import get_user_by_email
from app.repositories.user_repository import get_user_by_username


def register_user(
    db: Session,
    username: str,
    email: str,
    password: str
):
    existing_email = get_user_by_email(db, email)

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    existing_username = get_user_by_username(db,username)

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    hashed_password = hash_password(password)

    user_data = {
        "username": username,
        "email": email,
        "password_hash": hashed_password
    }

    return create_user(db, user_data)


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    return user


def login_user(
    db: Session,
    email: str,
    password: str
):
    user = authenticate_user(
        db,
        email,
        password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }