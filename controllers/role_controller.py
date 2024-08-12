from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from utils.response import create_response
from middlewares.authentication_middleware import authenticate_user
from utils.APIRouteList import (
    DELETE_ROLE_BY_ID,
    GET_ALL_ROLE_LIST,
    GET_ROLE_BY_ID,
    ROLE_CREATE_API,
    UPDATE_ROLE_BY_ID,
)
from schemas.response_schemas import API_Response
from models.user_roles_model import User_Role
from schemas.user_roles_schema import UserRoleCreate, UserRoleResponse, UserRoleUpdate
from services.role_services import (
    create_role,
    delete_user_role_by_id,
    get_all_user_roles,
    get_user_role_details_by_id,
    user_role_details_update,
)
from utils.messages import SOMETHING_WENT_WRONG
from models.users_model import User

router = APIRouter()

# API to create user role


@router.post(ROLE_CREATE_API, response_model=API_Response)
def create_new_role(
    role: UserRoleCreate,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    if not isinstance(user, User):  # Check if the response is a dict (error)
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        db_user_role = create_role(db, role)
        if not db_user_role["success"]:
            return create_response(
                db_user_role["status_code"],
                db_user_role["success"],
                db_user_role["message"],
            )

        user_response = UserRoleResponse.from_orm(db_user_role["data"])
        return create_response(
            status_code=db_user_role["status_code"],
            success=db_user_role["success"],
            message=db_user_role["message"],
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
            message=SOMETHING_WENT_WRONG,
        )


@router.get(GET_ALL_ROLE_LIST, response_model=API_Response)
def list_user_roles(
    sort_by: str = "name",
    order: str = "asc",
    skip: int = 0,
    limit: int = 10,
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
        result = get_all_user_roles(
            db, sort_by=sort_by, order=order, skip=skip, limit=limit
        )
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
            message=SOMETHING_WENT_WRONG,
        )


@router.get(f"{GET_ROLE_BY_ID}" + "{role_id}", response_model=API_Response)
def get_user_role_controller_by_id(
    role_id: int,
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
        result = get_user_role_details_by_id(db, role_id)
        if not result["success"]:
            return create_response(
                result["status_code"],
                result["success"],
                result["message"],
            )

        user_response = UserRoleResponse.from_orm(result["data"])
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=user_response,
        )
    except Exception as e:
        return create_response(
            status_code=500,
            success=False,
            message=SOMETHING_WENT_WRONG,
        )


@router.put(f"{UPDATE_ROLE_BY_ID}" + "{role_id}", response_model=API_Response)
def update_user_role_details(
    role_id: int,
    role_update: UserRoleUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):

    if not isinstance(user, User):  # Check if the response is a dict (error)
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )
    try:
        result = user_role_details_update(db, role_id, user_role_update=role_update)
        if not result["success"]:
            return create_response(
                result["status_code"],
                result["success"],
                result["message"],
            )

        user_response = UserRoleResponse.from_orm(result["data"])
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=user_response,
        )
    except Exception as e:
        return create_response(
            status_code=500,
            success=False,
            message=SOMETHING_WENT_WRONG,
        )


@router.delete(f"{DELETE_ROLE_BY_ID}" + "{role_id}", response_model=API_Response)
def delete_user_role_by_id_controller(
    role_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    if not isinstance(user, User):  # Check if the response is a dict (error)
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        result = delete_user_role_by_id(db, role_id)
        return create_response(
            result["status_code"],
            result["success"],
            result["message"],
        )
    except Exception as e:
        return create_response(
            status_code=500,
            success=False,
            message=SOMETHING_WENT_WRONG,
        )
