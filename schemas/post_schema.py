from pydantic import BaseModel, constr, validator
from typing import Optional, List
from utils.messages import USER_NAME_MUST_CONTAIN_ONLY_LETTERS
from schemas.post_category_schema import PostCategoryCreate
from schemas.post_tag_schema import PostTagCreate
from schemas.user_schemas import UserResponse
from schemas.category_schema import CategoryResponse
from schemas.tag_schema import TagResponse


class PostCreate(BaseModel):
    title: constr(min_length=3, max_length=50)
    content: str
    status: Optional[str] = "draft"
    categories: Optional[List[PostCategoryCreate]] = []
    tags: Optional[List[PostTagCreate]] = []
    user_id:int

    # @validator("title")
    # def name_must_contain_only_letters(cls, v):
    #     if not v.replace(" ", "").isalpha():
    #         raise ValueError(USER_NAME_MUST_CONTAIN_ONLY_LETTERS)
    #     return v.title()


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    status: str
    user_data: UserResponse
    category_data: CategoryResponse
    tag_data: TagResponse

    class Config:
        orm_mode = True
        from_attributes = True
