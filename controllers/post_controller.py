from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from utils.response import create_response
from middlewares.authentication_middleware import authenticate_user
from schemas.response_schemas import API_Response
from utils.messages import SOMETHING_WENT_WRONG
from utils.APIRouteList import GET_ALL_POST_LIST, POST_CREATE_API
from schemas.post_schema import PostCreate, PostResponse
from models.users_model import User
from services.post_services import create_post, get_all_posts_list


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
def list_user_roles(
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
