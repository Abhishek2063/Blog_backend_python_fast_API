from sqlalchemy.orm import Session
from fastapi import status
from sqlalchemy import asc, desc
from schemas.category_schema import CategoryCreate, CategoryResponse, CategoryUpdate
from utils.commonfunction import (
    check_category_contained_in_post_Category_table,
    get_category_by_id,
    get_category_by_name,
)
from utils.messages import (
    CATEGORY_CREATED_SUCCESSFULLY,
    CATEGORY_DELETE_SUCCESSFULLY,
    CATEGORY_FOUND_SUCCESSFULL,
    CATEGORY_IS_CONNECTED_WITH_USER_TABLE,
    CATEGORY_LIST_GET_SUCCESSFULLY,
    CATEGORY_NAME_ALREADY_TAKEN,
    CATEGORY_NOT_EXIST,
    CATEGORY_UPDATE_SUCCESSFULLY,
    INVALID_SORT_FIELD,
    INVALID_SORT_ORDER,
)
from models.categories_model import Category


#  create category
def create_category(db: Session, category: CategoryCreate):
    db_category = get_category_by_name(db, name=category.name)

    if db_category:
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": CATEGORY_NAME_ALREADY_TAKEN,
        }

    db_category = Category(
        name=category.name,
        description=category.description,
    )

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": CATEGORY_CREATED_SUCCESSFULLY,
        "data": db_category,
    }


# get all category with sorting and pagination
def get_all_category(
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
        "name": Category.name,
    }.get(sort_by, Category.name)

    order_method = asc if order == "asc" else desc

    query = db.query(Category).order_by(order_method(sort_column))

    total = query.count()
    categories = query.offset(skip).limit(limit).all()
    total_pages = (total + limit - 1) // limit
    current_page = skip // limit + 1

    return {
        "success": True,
        "status_code": 200,
        "message": CATEGORY_LIST_GET_SUCCESSFULLY,
        "data": {
            "total": total,
            "limit": limit,
            "skip": skip,
            "sort_by": sort_by,
            "sort_order": order,
            "total_pages": total_pages,
            "current_page": current_page,
            "result": [CategoryResponse.from_orm(category) for category in categories],
        },
    }


# get category details by ID
def get_category_details_by_id(db: Session, category_id: int):
    role = get_category_by_id(db, category_id)
    if not role:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": CATEGORY_NOT_EXIST,
        }
    return {
        "success": True,
        "status_code": 200,
        "message": CATEGORY_FOUND_SUCCESSFULL,
        "data": role,
    }


# to update the category details


def category_details_update(
    db: Session, category_id: int, category_update: CategoryUpdate
):
    db_category = get_category_by_id(db, category_id)
    if not db_category:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": CATEGORY_NOT_EXIST,
        }

    # Check if the new name is already taken by another role
    if category_update.name:
        existing_category = get_category_by_name(db, name=category_update.name)
        if existing_category:
            return {
                "success": False,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": CATEGORY_NAME_ALREADY_TAKEN,
            }

        # Update the role's name if it's provided and unique
        db_category.name = category_update.name

    # Update other fields if provided
    if category_update.description:
        db_category.description = category_update.description

    # Commit the changes to the database
    db.commit()
    db.refresh(db_category)

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": CATEGORY_UPDATE_SUCCESSFULLY,
        "data": db_category,
    }


# delete category data


def delete_category_by_id(db: Session, category_id: int):
    category = get_category_by_id(db, category_id)
    if not category:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": CATEGORY_NOT_EXIST,
        }
    category_check = check_category_contained_in_post_Category_table(db, category_id)
    if category_check:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": CATEGORY_IS_CONNECTED_WITH_USER_TABLE,
        }
    db.delete(category)
    db.commit()

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": CATEGORY_DELETE_SUCCESSFULLY,
    }
