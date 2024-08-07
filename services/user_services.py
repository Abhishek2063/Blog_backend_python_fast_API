from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from models.users_model import User
from schemas.user_schemas import UserCreate
from models.user_roles_model import User_Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    print("----"*50 , user , "user")
    db_user = get_user_by_email(db, email=user.email)
    print("----"*50 , db_user , "db_user")
    
    if db_user:
        return HTTPException(status_code=400, detail="Email already registered")
    print("----"*50 , db_user , "db_user")

    # Check if the role exists
    role = db.query(User_Role).filter(User_Role.id == user.role_id).first()
    
    print("----"*50 , role , "role")
    
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role_id")

    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=hashed_password,
        role_id=user.role_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
