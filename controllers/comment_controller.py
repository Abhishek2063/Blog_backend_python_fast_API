from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from utils.response import create_response
from middlewares.authentication_middleware import authenticate_user
from schemas.response_schemas import API_Response
from utils.APIRouteList import COMMENT_CREATE_API
from schemas.comment_schema import CommentCreate, CommentResponse
from models.users_model import User
from services.comment_services import create_comment
from utils.messages import SOMETHING_WENT_WRONG


router = APIRouter()

# API to create user role


@router.post(COMMENT_CREATE_API, response_model=API_Response)
def create_comment_controller(
    comment: CommentCreate,
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
        db_comment = create_comment(db, comment)
        if not db_comment["success"]:
            return create_response(
                db_comment["status_code"],
                db_comment["success"],
                db_comment["message"],
            )

        user_response = CommentResponse.from_orm(db_comment["data"])
        return create_response(
            status_code=db_comment["status_code"],
            success=db_comment["success"],
            message=db_comment["message"],
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
