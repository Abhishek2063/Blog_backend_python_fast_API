from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from models.users_model import User
from schemas.user_schemas import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserUpdatePassword,
)
from models.user_roles_model import User_Role
from utils.response import raise_http_exception
from utils.messages import (
    INVALID_SORT_FIELD,
    INVALID_SORT_ORDER,
    PASSWORD_NOT_MATCH,
    PASSWORD_UPDATE_SUCCESSFULLY,
    USER_CREATED_SUCCESSFULLY,
    USER_DATA_FOUND,
    USER_DELETED_SUCCESSFULLY,
    USER_EMAIL_ALREADY_REGISTERED,
    USER_INVALID_ROLE_ID,
    USER_NOT_EXIST,
    USER_UPDATE_SUCCESSFULLY,
    USERS_RETRIEVED_SUCCESSFULLY,
)
from utils.commonfunction import (
    get_role_by_id,
    get_user_by_email,
    get_user_by_id,
    verify_password,
)
from sqlalchemy import asc, desc

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# create user services
def create_user(db: Session, user: UserCreate):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": USER_EMAIL_ALREADY_REGISTERED,
        }

    role = get_role_by_id(db, user.role_id)
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


# get all users with sorting and pagination
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


# get the specific user details
def get_user_services_by_id(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
        }
    return {
        "success": True,
        "status_code": 200,
        "message": USER_DATA_FOUND,
        "data": user,
    }


# to update the user details


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    # Fetch the user by ID
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
        }

    # Validate and update the role if provided
    if user_update.role_id:
        role = get_role_by_id(db, user_update.role_id)
        if not role:
            return {
                "success": False,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": USER_INVALID_ROLE_ID,
            }
        db_user.role_id = user_update.role_id

    # Update other fields if provided
    if user_update.first_name:
        db_user.first_name = user_update.first_name
    if user_update.last_name:
        db_user.last_name = user_update.last_name
    if user_update.email:
        db_user.email = user_update.email

    # Commit the changes to the database
    db.commit()
    db.refresh(db_user)

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": USER_UPDATE_SUCCESSFULLY,
        "data": db_user,
    }


def update_user_password(
    db: Session, user_id: int, user_update_passowrd: UserUpdatePassword
):
    # Fetch the user by ID
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
        }

    if verify_password(user_update_passowrd.current_password, db_user.password_hash):
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": PASSWORD_NOT_MATCH,
        }

    # Update password
    hashed_password = pwd_context.hash(user_update_passowrd.current_password)
    db_user.password = hashed_password

    # Commit the changes to the database
    db.commit()
    db.refresh(db_user)

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": PASSWORD_UPDATE_SUCCESSFULLY,
        "data": db_user,
    }


def delete_user_by_id(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
        }

    db.delete(user)
    db.commit()

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": USER_DELETED_SUCCESSFULLY,
    }
