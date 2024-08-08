from sqlalchemy.orm import Session
from models.users_model import User
from utils.auth import create_access_token
from schemas.user_login_schema import UserLogin, UserLoginResponse
from fastapi import HTTPException, status
from utils.commonfunction import get_user_by_email, verify_password
from utils.messages import INVALID_CREDENTIALS, LOGIN_SUCCESSFUL


def login_user(db: Session, user: UserLogin):
    db_user = get_user_by_email(db, email=user.email)
    if not db_user:
        return {
            "success": False,
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "message": INVALID_CREDENTIALS,
        }

    if not verify_password(user.password, db_user.password_hash):
        return {
            "success": False,
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "message": INVALID_CREDENTIALS,
        }

    # Generate JWT token
    token = create_access_token(data={"sub": db_user.email})

    # Store token in database
    db_user.token = token
    db.commit()

    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": LOGIN_SUCCESSFUL,
        "data": UserLoginResponse(
            id=db_user.id,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            email=db_user.email,
            role=db_user.role,
            token=token,
        ),
    }
