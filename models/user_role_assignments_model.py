from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User_Role_Assignment(Base):
    __tablename__ = "user_role_assignments"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    role_id = Column(
        Integer, ForeignKey("user_roles.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    users = relationship("User", back_populates="user_role_assignments")
    user_roles = relationship("User_Role", back_populates="user_role_assignments")
