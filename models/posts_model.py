from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    title = Column(String(20), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    status = Column(
        Enum("draft", "published", "archived", name="post_status"), default="draft"
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    users = relationship("User", back_populates="posts")
    post_categories = relationship(
        "Post_Category",
        back_populates="posts",
        cascade="all, delete, delete-orphan",
    )
    comments = relationship(
        "Comment", back_populates="posts", cascade="all, delete, delete-orphan"
    )
    post_tags = relationship(
        "Post_Tag", back_populates="posts", cascade="all, delete, delete-orphan"
    )
