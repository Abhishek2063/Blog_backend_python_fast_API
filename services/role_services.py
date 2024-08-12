from sqlalchemy.orm import Session
from schemas.user_roles_schema import UserRoleCreate, UserRoleResponse, UserRoleUpdate
from utils.commonfunction import (
    check_user_role_contained_in_user_table,
    get_role_by_id,
    get_user_role_by_name,
)
from fastapi import status
from utils.messages import (
    INVALID_SORT_FIELD,
    INVALID_SORT_ORDER,
    USER_ROLE_CREATED_SUCCESSFULLY,
    USER_ROLE_DELETE_SUCCESSFULLY,
    USER_ROLE_FOUND_SUCCESSFULL,
    USER_ROLE_IS_CONNECTED_WITH_USER_TABLE,
    USER_ROLE_NAME_ALREADY_TAKEN,
    USER_ROLE_NOT_EXIST,
    USER_ROLE_UPDATE_SUCCESSFULLY,
    USER_ROLES_LIST_GET_SUCCESSFULLY,
)
from models.user_roles_model import User_Role
from sqlalchemy import asc, desc


#  create role
def create_role(db: Session, role: UserRoleCreate):
    db_user_role = get_user_role_by_name(db, name=role.name)

    if db_user_role:
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": USER_ROLE_NAME_ALREADY_TAKEN,
        }

    db_user_role = User_Role(
        name=role.name,
        description=role.description,
    )

    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)

    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": USER_ROLE_CREATED_SUCCESSFULLY,
        "data": db_user_role,
    }


# get all user roles with sorting and pagination
def get_all_user_roles(
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
        "name": User_Role.name,
    }.get(sort_by, User_Role.name)

    order_method = asc if order == "asc" else desc

    query = db.query(User_Role).order_by(order_method(sort_column))

    total = query.count()
    user_roles = query.offset(skip).limit(limit).all()
    total_pages = (total + limit - 1) // limit
    current_page = skip // limit + 1

    return {
        "success": True,
        "status_code": 200,
        "message": USER_ROLES_LIST_GET_SUCCESSFULLY,
        "data": {
            "total": total,
            "limit": limit,
            "skip": skip,
            "sort_by": sort_by,
            "sort_order": order,
            "total_pages": total_pages,
            "current_page": current_page,
            "user_roles": [UserRoleResponse.from_orm(role) for role in user_roles],
        },
    }


# get user roles details by ID
def get_user_role_details_by_id(db: Session, role_id: int):
    role = get_role_by_id(db, role_id)
    if not role:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_ROLE_NOT_EXIST,
        }
    return {
        "success": True,
        "status_code": 200,
        "message": USER_ROLE_FOUND_SUCCESSFULL,
        "data": role,
    }


# to update the user role details


def user_role_details_update(
    db: Session, role_id: int, user_role_update: UserRoleUpdate
):
    db_user_role = get_role_by_id(db, role_id)
    if not db_user_role:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_ROLE_NOT_EXIST,
        }

    # Check if the new name is already taken by another role
    if user_role_update.name:
        existing_role = get_user_role_by_name(db, name=user_role_update.name)
        if existing_role:
            return {
                "success": False,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": USER_ROLE_NAME_ALREADY_TAKEN,
            }

        # Update the role's name if it's provided and unique
        db_user_role.name = user_role_update.name

    # Update other fields if provided
    if user_role_update.description:
        db_user_role.description = user_role_update.description

    # Commit the changes to the database
    db.commit()
    db.refresh(db_user_role)

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": USER_ROLE_UPDATE_SUCCESSFULLY,
        "data": db_user_role,
    }


# delete user role data


def delete_user_role_by_id(db: Session, role_id: int):
    role = get_role_by_id(db, role_id)
    if not role:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_ROLE_NOT_EXIST,
        }
    role_check = check_user_role_contained_in_user_table(db, role_id)
    if role_check:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_ROLE_IS_CONNECTED_WITH_USER_TABLE,
        }
    db.delete(role)
    db.commit()

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": USER_ROLE_DELETE_SUCCESSFULLY,
    }
