from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from utils.response import create_response
from middlewares.authentication_middleware import authenticate_user
from schemas.response_schemas import API_Response
from utils.messages import SOMETHING_WENT_WRONG
from models.users_model import User
from utils.APIRouteList import (
    CATEGORY_CREATE_API,
    DELETE_CATEGORY_BY_ID,
    GET_ALL_CATEGORY_LIST,
    GET_CATEGORY_BY_ID,
    UPDATE_CATEGORY_BY_ID,
)
from schemas.category_schema import CategoryCreate, CategoryResponse, CategoryUpdate
from services.category_services import (
    category_details_update,
    create_category,
    delete_category_by_id,
    get_all_category,
    get_category_details_by_id,
)
from utils.commonfunction import get_category_by_id


router = APIRouter()

# API to create category


@router.post(CATEGORY_CREATE_API, response_model=API_Response)
def create_new_role(
    category: CategoryCreate,
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
        category_response = create_category(db, category)
        if not category_response["success"]:
            return create_response(
                category_response["status_code"],
                category_response["success"],
                category_response["message"],
            )

        category_schema_response = CategoryResponse.from_orm(category_response["data"])
        return create_response(
            status_code=category_response["status_code"],
            success=category_response["success"],
            message=category_response["message"],
            data=category_schema_response,
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


@router.get(GET_ALL_CATEGORY_LIST, response_model=API_Response)
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
        result = get_all_category(
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


@router.get(f"{GET_CATEGORY_BY_ID}" + "{category_id}", response_model=API_Response)
def get_user_role_controller_by_id(
    category_id: int,
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
        result = get_category_details_by_id(db, category_id)
        if not result["success"]:
            return create_response(
                result["status_code"],
                result["success"],
                result["message"],
            )

        categoryresponse = CategoryResponse.from_orm(result["data"])
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=categoryresponse,
        )
    except Exception as e:
        return create_response(
            status_code=500,
            success=False,
            message=SOMETHING_WENT_WRONG,
        )


@router.put(f"{UPDATE_CATEGORY_BY_ID}" + "{category_id}", response_model=API_Response)
def update_user_role_details(
    category_id: int,
    category_update: CategoryUpdate,
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
        result = category_details_update(db, category_id, category_update)
        if not result["success"]:
            return create_response(
                result["status_code"],
                result["success"],
                result["message"],
            )

        categoryresponse = CategoryResponse.from_orm(result["data"])
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=categoryresponse,
        )
    except Exception as e:
        return create_response(
            status_code=500,
            success=False,
            message=SOMETHING_WENT_WRONG,
        )


@router.delete(
    f"{DELETE_CATEGORY_BY_ID}" + "{category_id}", response_model=API_Response
)
def delete_user_role_by_id_controller(
    category_id: int,
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
        result = delete_category_by_id(db, category_id)
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
