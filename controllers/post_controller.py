from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from utils.response import create_response
from middlewares.authentication_middleware import authenticate_user
from schemas.response_schemas import API_Response
from utils.messages import SOMETHING_WENT_WRONG
from utils.APIRouteList import (
    DELETE_POST_BY_ID,
    GET_ALL_POST_LIST,
    GET_ALL_USER_POST_LIST,
    GET_POST_BY_ID,
    POST_CREATE_API,
    UPDATE_POST_BY_ID,
)
from schemas.post_schema import PostCreate, PostResponse
from models.users_model import User
from services.post_services import (
    create_post,
    delete_post,
    get_all_posts_list,
    get_post_details_by_id,
    get_user_posts,
    update_post,
)


router = APIRouter()


# API to create post
@router.post(POST_CREATE_API, response_model=API_Response)
def create_new_post(
    post: PostCreate,
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
        post_response = create_post(db, post)
        if not post_response["success"]:
            return create_response(
                post_response["status_code"],
                post_response["success"],
                post_response["message"],
            )

        tag_schema_response = PostResponse.from_orm(post_response["data"])
        return create_response(
            status_code=post_response["status_code"],
            success=post_response["success"],
            message=post_response["message"],
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


@router.get(GET_ALL_POST_LIST, response_model=API_Response)
def list_post(
    sort_by: str = "title",
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
        result = get_all_posts_list(
            db, sort_by=sort_by, order=order, skip=skip, limit=limit
        )
        if not result["success"]:
            return create_response(
                result["status_code"],
                result["success"],
                result["message"],
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


@router.get(f"{GET_ALL_USER_POST_LIST}" + "{user_id}", response_model=API_Response)
def list_post_users(
    user_id: int,
    sort_by: str = "title",
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
        result = get_user_posts(
            db, user_id, sort_by=sort_by, order=order, skip=skip, limit=limit
        )

        if not result["success"]:
            return create_response(
                result["status_code"],
                result["success"],
                result["message"],
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


@router.get(f"{GET_POST_BY_ID}" + "{post_id}", response_model=API_Response)
def get_post_by_id_controller(
    post_id: int,
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
        result = get_post_details_by_id(db, post_id)
        if not result["success"]:
            return create_response(
                result["status_code"],
                result["success"],
                result["message"],
            )

        post_response = PostResponse.from_orm(result["data"])
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=post_response,
        )
    except Exception as e:
        return create_response(
            status_code=500,
            success=False,
            message=SOMETHING_WENT_WRONG,
        )


@router.put(f"{UPDATE_POST_BY_ID}" + "{post_id}", response_model=API_Response)
def update_user_role_details(
    post_id: int,
    post_update: PostCreate,
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
        result = update_post(db, post_id, post_update)
        if not result["success"]:
            return create_response(
                result["status_code"],
                result["success"],
                result["message"],
            )

        post_response = PostResponse.from_orm(result["data"])
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=post_response,
        )
    except Exception as e:
        return create_response(
            status_code=500,
            success=False,
            message=SOMETHING_WENT_WRONG,
        )


@router.delete(f"{DELETE_POST_BY_ID}" + "{post_id}", response_model=API_Response)
def delete_user_role_by_id_controller(
    post_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    if not isinstance(user, User):  # Check if the response is a dict (error)
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    # try:
    result = delete_post(db, post_id)
    return create_response(
        result["status_code"],
        result["success"],
        result["message"],
    )
    # except Exception as e:
    #     return create_response(
    #         status_code=500,
    #         success=False,
    #         message=SOMETHING_WENT_WRONG,
    #     )
