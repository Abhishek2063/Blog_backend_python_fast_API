from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from utils.response import create_response
from middlewares.authentication_middleware import authenticate_user
from schemas.response_schemas import API_Response
from utils.messages import SOMETHING_WENT_WRONG
from models.users_model import User
from schemas.tag_schema import TagCreate, TagResponse, TagUpdate
from services.tag_services import (
    create_tag,
    delete_tag_by_id,
    get_all_tag_roles,
    get_tag_details_by_id,
    tag_details_update,
)
from utils.APIRouteList import (
    DELETE_TAG_BY_ID,
    GET_ALL_TAG_LIST,
    GET_TAG_BY_ID,
    TAG_CREATE_API,
    UPDATE_TAG_BY_ID,
)

router = APIRouter()

# API to create tag


@router.post(TAG_CREATE_API, response_model=API_Response)
def create_new_role(
    tag: TagCreate,
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
        tag_response = create_tag(db, tag)
        if not tag_response["success"]:
            return create_response(
                tag_response["status_code"],
                tag_response["success"],
                tag_response["message"],
            )

        tag_schema_response = TagResponse.from_orm(tag_response["data"])
        return create_response(
            status_code=tag_response["status_code"],
            success=tag_response["success"],
            message=tag_response["message"],
            data=tag_schema_response,
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


@router.get(GET_ALL_TAG_LIST, response_model=API_Response)
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
        result = get_all_tag_roles(
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


@router.get(f"{GET_TAG_BY_ID}" + "{tag_id}", response_model=API_Response)
def get_user_role_controller_by_id(
    tag_id: int,
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
        result = get_tag_details_by_id(db, tag_id)
        if not result["success"]:
            return create_response(
                result["status_code"],
                result["success"],
                result["message"],
            )

        tag_response = TagResponse.from_orm(result["data"])
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=tag_response,
        )
    except Exception as e:
        return create_response(
            status_code=500,
            success=False,
            message=SOMETHING_WENT_WRONG,
        )


@router.put(f"{UPDATE_TAG_BY_ID}" + "{tag_id}", response_model=API_Response)
def update_user_role_details(
    tag_id: int,
    tag_update: TagUpdate,
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
        result = tag_details_update(db, tag_id, tag_update)
        if not result["success"]:
            return create_response(
                result["status_code"],
                result["success"],
                result["message"],
            )

        tag_response = TagResponse.from_orm(result["data"])
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=tag_response,
        )
    except Exception as e:
        return create_response(
            status_code=500,
            success=False,
            message=SOMETHING_WENT_WRONG,
        )


@router.delete(f"{DELETE_TAG_BY_ID}" + "{tag_id}", response_model=API_Response)
def delete_user_role_by_id_controller(
    tag_id: int,
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
        result = delete_tag_by_id(db, tag_id)
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
