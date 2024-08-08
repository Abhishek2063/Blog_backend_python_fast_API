from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user_schemas import UserCreate, UserResponse
from app.database import get_db
from utils.response import create_response
from services.user_services import create_user
from schemas.response_schemas import API_Response
from utils.messages import USER_CREATION_FAILED
from utils.APIRouteList import USER_CREATE_API

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
