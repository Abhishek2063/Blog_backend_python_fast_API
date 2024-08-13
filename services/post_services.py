from sqlalchemy.orm import Session
from schemas.post_schema import PostCreate
from models.posts_model import Post
from models.post_categories_model import Post_Category
from models.post_tags_model import Post_Tag
from fastapi import status
from utils.messages import (
    CATEGORY_NOT_FOUND,
    POST_CREATED_SUCCESSFULLY,
    POST_NAME_ALREADY_TAKEN,
    TAG_NOT_FOUND,
)
from utils.commonfunction import get_category_by_id, get_post_by_title, get_tag_by_id


# create post
def create_post(db: Session, post_create: PostCreate):
    db_post = get_post_by_title(db, title=post_create.title)

    if db_post:
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": POST_NAME_ALREADY_TAKEN,
        }

    # Check if all categories exist
    for category in post_create.categories:
        db_category = get_category_by_id(db, category.category_id)
        if not db_category:
            return {
                "success": False,
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": CATEGORY_NOT_FOUND,
            }

    # Check if all tags exist
    for tag in post_create.tags:
        db_tag = get_tag_by_id(db, tag.tag_id)
        if not db_tag:
            return {
                "success": False,
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": TAG_NOT_FOUND,
            }

    db_post = Post(
        title=post_create.title,
        content=post_create.content,
        status=post_create.status,
        user_id=post_create.user_id,
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    # Handle Categories
    for category in post_create.categories:
        db_post_category = Post_Category(
            post_id=db_post.id, category_id=category.category_id
        )
        db.add(db_post_category)

    # Handle Tags
    for tag in post_create.tags:
        db_post_tag = Post_Tag(post_id=db_post.id, tag_id=tag.tag_id)
        db.add(db_post_tag)

    db.commit()

    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": POST_CREATED_SUCCESSFULLY,
        "data": db_post,
    }
