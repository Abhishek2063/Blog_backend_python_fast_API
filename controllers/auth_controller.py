from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from utils.response import create_response
from schemas.response_schemas import API_Response
from schemas.user_login_schema import UserLogin
from services.auth_services import login_user
from utils.messages import INTERNAL_SERVER_ERROR, LOGIN_SUCCESSFUL

router = APIRouter()


@router.post(
    "/login/",
    response_model=API_Response,
    responses={
        400: {"model": API_Response},
        401: {"model": API_Response},
        500: {"model": API_Response},
        200: {"model": API_Response},
    },
)
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        login_response = login_user(db, user)
        return create_response(
            status_code=login_response.get("status_code", 200),
            success=login_response.get("success", True),
            message=login_response.get("message", LOGIN_SUCCESSFUL),
            data=login_response.get("data", None),
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
            message=INTERNAL_SERVER_ERROR,
        )
