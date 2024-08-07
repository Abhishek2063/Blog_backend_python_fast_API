from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(20), nullable=False, unique=True)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    post_tags = relationship(
        "Post_Tag", back_populates="tags", cascade="all, delete, delete-orphan"
    )
