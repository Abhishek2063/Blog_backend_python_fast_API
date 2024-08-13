from sqlalchemy.orm import Session
from fastapi import status
from schemas.comment_schema import CommentCreate
from utils.commonfunction import get_post_by_id, get_user_by_id
from utils.messages import COMMENT_CREATED_SUCCESSFULLY, POST_NOT_EXIST, USER_NOT_EXIST
from models.comments_model import Comment


def create_comment(db: Session, comment: CommentCreate):
    post_details = get_post_by_id(db, comment.post_id)

    if not post_details:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": POST_NOT_EXIST,
        }

    # Fetch the user data
    user = get_user_by_id(db, user_id=comment.user_id)
    if not user:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
        }

    db_comment = Comment(
        user_id=comment.user_id,
        post_id=comment.post_id,
        content=comment.content,
    )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": COMMENT_CREATED_SUCCESSFULLY,
        "data": db_comment,
    }
