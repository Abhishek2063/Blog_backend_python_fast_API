from sqlalchemy.orm import Session
from fastapi import status

from sqlalchemy import asc, desc
from schemas.tag_schema import TagCreate, TagResponse, TagUpdate
from utils.commonfunction import (
    check_tag_contained_in_post_tag_table,
    get_tag_by_id,
    get_tag_by_name,
)
from utils.messages import (
    INVALID_SORT_FIELD,
    INVALID_SORT_ORDER,
    TAG_CREATED_SUCCESSFULLY,
    TAG_DELETE_SUCCESSFULLY,
    TAG_FOUND_SUCCESSFULL,
    TAG_IS_CONNECTED_WITH_USER_TABLE,
    TAG_NAME_ALREADY_TAKEN,
    TAG_NOT_EXIST,
    TAG_UPDATE_SUCCESSFULLY,
    TAGS_LIST_GET_SUCCESSFULLY,
)
from models.tags_model import Tag


#  create tag
def create_tag(db: Session, tag: TagCreate):
    db_tag = get_tag_by_name(db, name=tag.name)

    if db_tag:
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": TAG_NAME_ALREADY_TAKEN,
        }

    db_tag = Tag(
        name=tag.name,
        description=tag.description,
    )

    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)

    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": TAG_CREATED_SUCCESSFULLY,
        "data": db_tag,
    }


# get all tag with sorting and pagination
def get_all_tag_roles(
    db: Session,
    sort_by: str = "name",
    order: str = "asc",
    skip: int = 0,
    limit: int = 10,
):
    valid_sort_by = ["name"]
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
        "name": Tag.name,
    }.get(sort_by, Tag.name)

    order_method = asc if order == "asc" else desc

    query = db.query(Tag).order_by(order_method(sort_column))

    total = query.count()
    user_roles = query.offset(skip).limit(limit).all()
    total_pages = (total + limit - 1) // limit
    current_page = skip // limit + 1

    return {
        "success": True,
        "status_code": 200,
        "message": TAGS_LIST_GET_SUCCESSFULLY,
        "data": {
            "total": total,
            "limit": limit,
            "skip": skip,
            "sort_by": sort_by,
            "sort_order": order,
            "total_pages": total_pages,
            "current_page": current_page,
            "user_roles": [TagResponse.from_orm(role) for role in user_roles],
        },
    }


# get tag details by ID
def get_tag_details_by_id(db: Session, tag_id: int):
    role = get_tag_by_id(db, tag_id)
    if not role:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": TAG_NOT_EXIST,
        }
    return {
        "success": True,
        "status_code": 200,
        "message": TAG_FOUND_SUCCESSFULL,
        "data": role,
    }


# to update the tag details


def tag_details_update(db: Session, tag_id: int, tag_update: TagUpdate):
    db_tag = get_tag_by_id(db, tag_id)
    if not db_tag:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": TAG_NOT_EXIST,
        }

    # Check if the new name is already taken by another role
    if tag_update.name:
        existing_tag = get_tag_by_name(db, name=tag_update.name)
        if existing_tag:
            return {
                "success": False,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": TAG_NAME_ALREADY_TAKEN,
            }

        # Update the role's name if it's provided and unique
        db_tag.name = tag_update.name

    # Update other fields if provided
    if tag_update.description:
        db_tag.description = tag_update.description

    # Commit the changes to the database
    db.commit()
    db.refresh(db_tag)

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": TAG_UPDATE_SUCCESSFULLY,
        "data": db_tag,
    }


# delete tag data


def delete_tag_by_id(db: Session, tag_id: int):
    tag = get_tag_by_id(db, tag_id)
    if not tag:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": TAG_NOT_EXIST,
        }
    tag_check = check_tag_contained_in_post_tag_table(db, tag_id)
    if tag_check:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": TAG_IS_CONNECTED_WITH_USER_TABLE,
        }
    db.delete(tag)
    db.commit()

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": TAG_DELETE_SUCCESSFULLY,
    }
