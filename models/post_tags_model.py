from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Post_Tag(Base):
    __tablename__ = "post_tags"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    tag_id = Column(
        Integer, ForeignKey("tags.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    post = relationship("Post", back_populates="tags")
    tag = relationship("Tag", back_populates="posts")
