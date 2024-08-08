from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user_schemas import UserCreate, UserResponse
from app.database import get_db
from utils.response import create_response
from services.user_services import create_user, get_user_services_by_id, get_users
from schemas.response_schemas import API_Response
from utils.messages import USER_CREATION_FAILED, USER_FOUND_BY_ID_ERROR
from utils.APIRouteList import (
    GET_ALL_USERS_LIST_WITH_PAGINATION,
    GET_USER_BY_ID_API,
    USER_CREATE_API,
)
from models.users_model import User
from models.user_roles_model import User_Role
from middlewares.authentication_middleware import authenticate_user

router = APIRouter()


@router.post(
    USER_CREATE_API,
    response_model=API_Response,
    responses={
        400: {"model": API_Response},
        500: {"model": API_Response},
        200: {"model": API_Response},
        201: {"model": API_Response},
    },
)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = create_user(db, user)

        if not db_user["success"]:
            return create_response(
                db_user["status_code"],
                db_user["success"],
                db_user["message"],
            )

        user_response = UserResponse.from_orm(db_user["data"])
        return create_response(
            status_code=db_user["status_code"],
            success=db_user["success"],
            message=db_user["message"],
            data=user_response,
        )
    except HTTPException as e:
        return create_response(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        return create_response(
            status_code=500,
            success=False,
            message=USER_CREATION_FAILED,
        )


@router.get(GET_ALL_USERS_LIST_WITH_PAGINATION, response_model=API_Response)
def list_users(
    sort_by: str = "email",
    order: str = "asc",
    skip: int = 0,
    limit: int = 2,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),  # Ensure user is authenticated
):
    if not isinstance(user, User):  # Check if the response is a dict (error)
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        result = get_users(db, sort_by=sort_by, order=order, skip=skip, limit=limit)
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=result["data"],
        )
    except Exception as e:
        return create_response(
            status_code=500,
            success=False,
            message=USER_CREATION_FAILED,
        )


@router.get(f"{GET_USER_BY_ID_API}" + "{user_id}", response_model=API_Response)
def get_user_controller_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),  # Ensure user is authenticated
):
    if not isinstance(user, User):  # Check if the response is a dict (error)
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        result = get_user_services_by_id(db, user_id)
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=result["data"],
        )
    except Exception as e:
        return create_response(
            status_code=500,
            success=False,
            message=USER_FOUND_BY_ID_ERROR,
        )
