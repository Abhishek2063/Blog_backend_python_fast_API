from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.users_model import User
from models.user_roles_model import User_Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_role_by_id(db: Session, role_id: int):
    return db.query(User_Role).filter(User_Role.id == role_id).first()