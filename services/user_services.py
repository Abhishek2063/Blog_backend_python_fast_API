from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from models.users_model import User
from schemas.user_schemas import UserCreate
from models.user_roles_model import User_Role
from utils.response import raise_http_exception
from utils.messages import (
    USER_CREATED_SUCCESSFULLY,
    USER_EMAIL_ALREADY_REGISTERED,
    USER_INVALID_ROLE_ID,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": USER_EMAIL_ALREADY_REGISTERED,
        }

    role = db.query(User_Role).filter(User_Role.id == user.role_id).first()
    if not role:
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": USER_INVALID_ROLE_ID,
        }

    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=hashed_password,
        role_id=user.role_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": USER_CREATED_SUCCESSFULLY,
        "data": db_user,
    }
