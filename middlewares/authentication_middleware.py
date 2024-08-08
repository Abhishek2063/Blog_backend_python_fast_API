from fastapi.security import OAuth2PasswordBearer
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from jose import JWTError, jwt
from app.config import settings
from models.users_model import User
from typing import Optional
from utils.messages import (
    EXPIRED_AUTHORIZATION_TOKEN,
    INVALID_AUTHORIZATION_TOKEN,
    MISSING_AUTHORIZATION_TOKEN,
)
from utils.commonfunction import get_user_by_email, get_user_by_id


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(
    token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    if token is None:
        return {
            "success": False,
            "status_code": 401,
            "message": MISSING_AUTHORIZATION_TOKEN,
        }

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

        user_email = payload.get("sub")

        if user_email is None:
            return {
                "success": False,
                "status_code": 401,
                "message": INVALID_AUTHORIZATION_TOKEN,
            }

        user = get_user_by_email(db, user_email)
        if user is None:
            return {
                "success": False,
                "status_code": 401,
                "message": INVALID_AUTHORIZATION_TOKEN,
            }

        return user
    except JWTError as e:
        if "expired" in str(e):
            return {
                "success": False,
                "status_code": 401,
                "message": EXPIRED_AUTHORIZATION_TOKEN,
            }

        else:
            return {
                "success": False,
                "status_code": 401,
                "message": INVALID_AUTHORIZATION_TOKEN,
            }
