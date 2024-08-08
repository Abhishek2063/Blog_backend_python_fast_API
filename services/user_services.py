from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from models.users_model import User
from schemas.user_schemas import UserCreate, UserResponse
from models.user_roles_model import User_Role
from utils.response import raise_http_exception
from utils.messages import (
    INVALID_SORT_FIELD,
    INVALID_SORT_ORDER,
    USER_CREATED_SUCCESSFULLY,
    USER_EMAIL_ALREADY_REGISTERED,
    USER_INVALID_ROLE_ID,
    USERS_RETRIEVED_SUCCESSFULLY,
)
from utils.commonfunction import get_user_by_email
from sqlalchemy import asc, desc

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def get_users(
    db: Session,
    sort_by: str = "email",
    order: str = "asc",
    skip: int = 0,
    limit: int = 10,
):
    valid_sort_by = ["email", "first_name", "last_name", "role"]
    valid_order = ["asc", "desc"]

    if sort_by not in valid_sort_by:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": INVALID_SORT_FIELD,
        }
    if order not in valid_order:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": INVALID_SORT_ORDER,
        }

    sort_column = {
        "email": User.email,
        "first_name": User.first_name,
        "last_name": User.last_name,
        "role": User_Role.name,
    }.get(sort_by, User.email)

    order_method = asc if order == "asc" else desc

    query = (
        db.query(User)
        .join(User_Role, User.role_id == User_Role.id)
        .order_by(order_method(sort_column))
    )

    total = query.count()
    users = query.offset(skip).limit(limit).all()
    total_pages = (total + limit - 1) // limit
    current_page = skip // limit + 1

    return {
        "success": True,
        "status_code": 200,
        "message": USERS_RETRIEVED_SUCCESSFULLY,
        "data": {
            "total": total,
            "limit": limit,
            "skip": skip,
            "sort_by": sort_by,
            "sort_order": order,
            "total_pages": total_pages,
            "current_page": current_page,
            "users": [UserResponse.from_orm(user) for user in users],
        },
    }
