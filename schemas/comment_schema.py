from pydantic import BaseModel, constr, validator
from typing import Optional, List
from utils.messages import USER_NAME_MUST_CONTAIN_ONLY_LETTERS



class CommentCreate(BaseModel):
    user_id:int
    post_id:int
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str

    class Config:
        orm_mode = True
        from_attributes = True
