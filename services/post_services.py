from sqlalchemy.orm import Session
from schemas.post_schema import PostCreate, PostResponse
from models.posts_model import Post
from models.post_categories_model import Post_Category
from models.post_tags_model import Post_Tag
from fastapi import status
from utils.messages import (
    CATEGORY_NOT_FOUND,
    INVALID_SORT_FIELD,
    INVALID_SORT_ORDER,
    POST_CREATED_SUCCESSFULLY,
    POST_LIST_GET_SUCCESSFULLY,
    POST_NAME_ALREADY_TAKEN,
    TAG_NOT_FOUND,
    USER_NOT_EXIST,
)
from utils.commonfunction import (
    get_category_by_id,
    get_post_by_title,
    get_tag_by_id,
    get_user_by_id,
)
from sqlalchemy import asc, desc
from sqlalchemy.orm import joinedload
from typing import List, Dict, Any
from schemas.user_schemas import UserResponse
from schemas.category_schema import CategoryResponse
from schemas.tag_schema import TagResponse


# create post
def create_post(db: Session, post_create: PostCreate):
    db_post = get_post_by_title(db, title=post_create.title)

    if db_post:
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": POST_NAME_ALREADY_TAKEN,
        }

    # Fetch the user data
    user = get_user_by_id(db, user_id=post_create.user_id)
    if not user:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
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

    categories = []
    tags = []

    # Handle Categories
    for category in post_create.categories:
        db_category = get_category_by_id(db, category.category_id)
        db_post_category = Post_Category(
            post_id=db_post.id, category_id=category.category_id
        )
        db.add(db_post_category)
        categories.append(db_category)

    # Handle Tags
    for tag in post_create.tags:
        db_tag = get_tag_by_id(db, tag.tag_id)
        db_post_tag = Post_Tag(post_id=db_post.id, tag_id=tag.tag_id)
        db.add(db_post_tag)
        tags.append(db_tag)

    db.commit()

    # Create a dictionary with the necessary data
    post_data = {
        "id": db_post.id,
        "title": db_post.title,
        "content": db_post.content,
        "status": db_post.status,
        "user": user,
        "categories": categories,
        "tags": tags,
    }

    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": POST_CREATED_SUCCESSFULLY,
        "data": post_data,
    }


# get all the post with sorting and pagination


def get_all_posts_list(
    db: Session,
    sort_by: str = "title",
    order: str = "asc",
    skip: int = 0,
    limit: int = 10,
) -> Dict[str, Any]:
    valid_sort_by = ["title", "status"]
    valid_order = ["asc", "desc"]
    if sort_by not in valid_sort_by:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": INVALID_SORT_FIELD,
        }
    if order not in valid_order:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": INVALID_SORT_ORDER,
        }
    sort_column = {
        "title": Post.title,
    }.get(sort_by, Post.title)

    order_method = asc if order == "asc" else desc

    query = db.query(Post).order_by(order_method(sort_column))

    total = query.count()
    post_list = query.offset(skip).limit(limit).all()
    total_pages = (total + limit - 1) // limit
    current_page = skip // limit + 1

    post_responses = []
    for post in post_list:
        post_response = PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            status=post.status,
            user=UserResponse.from_orm(post.user),
            categories=[
                CategoryResponse.from_orm(pc.category) for pc in post.categories
            ],
            tags=[TagResponse.from_orm(pt.tag) for pt in post.tags],
        )
        post_responses.append(post_response)
    return {
        "success": True,
        "status_code": 200,
        "message": POST_LIST_GET_SUCCESSFULLY,
        "data": {
            "total": total,
            "limit": limit,
            "skip": skip,
            "sort_by": sort_by,
            "sort_order": order,
            "total_pages": total_pages,
            "current_page": current_page,
            "result": post_responses,
        },
    }
