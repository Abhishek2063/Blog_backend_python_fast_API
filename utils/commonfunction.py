from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.users_model import User
from models.user_roles_model import User_Role
from models.tags_model import Tag
from models.post_tags_model import Post_Tag

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_role_by_id(db: Session, role_id: int):
    return db.query(User_Role).filter(User_Role.id == role_id).first()


def get_user_role_by_name(db: Session, name: str):
    return db.query(User_Role).filter(User_Role.name == name).first()


def check_user_role_contained_in_user_table(db: Session, role_id: int):
    return db.query(User).filter(User.role_id == role_id).first()


def get_tag_by_name(db: Session, name: str):
    return db.query(Tag).filter(Tag.name == name).first()


def get_tag_by_id(db: Session, tag_id: int):
    return db.query(Tag).filter(Tag.id == tag_id).first()


def check_tag_contained_in_post_tag_table(db: Session, tag_id: int):
    return db.query(Post_Tag).filter(Post_Tag.tag_id == tag_id).first()
