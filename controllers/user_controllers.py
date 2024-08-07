from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user_schemas import UserCreate, UserResponse
from app.database import get_db
from utils.response import create_response
from services.user_services import create_user

router = APIRouter()

@router.post("/create/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = create_user(db, user)
        return create_response(
            status_code=201,
            success=True,
            message="User created successfully",
            data=UserResponse.from_orm(db_user)
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
            message="An error occurred while creating the user",
        )