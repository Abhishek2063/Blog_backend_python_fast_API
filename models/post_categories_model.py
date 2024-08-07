from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Post_Category(Base):
    __tablename__ = "post_categories"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    posts = relationship("Post", back_populates="post_categories")
    categories = relationship("Category", back_populates="post_categories")
