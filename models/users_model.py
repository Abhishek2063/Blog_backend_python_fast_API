from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    first_name = Column(String(20), nullable=False, unique=False)
    last_name = Column(String(20), nullable=True, unique=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    posts = relationship(
        "Post", back_populates="users", cascade="all, delete, delete-orphan"
    )
    comments = relationship(
        "Comment", back_populates="users", cascade="all, delete, delete-orphan"
    )
    user_role_assignments = relationship(
        "User_Role_Assignment",
        back_populates="users",
        cascade="all, delete, delete-orphan",
    )
