from pydantic import BaseModel

class PostCategoryCreate(BaseModel):
    category_id: int