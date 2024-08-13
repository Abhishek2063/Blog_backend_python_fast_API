from pydantic import BaseModel

class PostTagCreate(BaseModel):
    tag_id: int