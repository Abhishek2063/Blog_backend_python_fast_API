from pydantic import BaseModel, constr, validator
from typing import Optional
from utils.messages import USER_NAME_MUST_CONTAIN_ONLY_LETTERS

class CategoryCreate(BaseModel):
    name: constr(min_length=2, max_length=20)
    description:Optional[constr(min_length=2, max_length=20)] = None
    
    @validator("name")
    def name_must_contain_only_letters(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError(USER_NAME_MUST_CONTAIN_ONLY_LETTERS)
        return v.title()

class CategoryUpdate(BaseModel):
    name: Optional[constr(min_length=2, max_length=20)] = None
    description:Optional[constr(min_length=2, max_length=20)] = None
    
    @validator("name")
    def name_must_contain_only_letters(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError(USER_NAME_MUST_CONTAIN_ONLY_LETTERS)
        return v.title()

class CategoryResponse(BaseModel):
    id:int
    name:str
    description:str
    
    class Config:
        orm_mode = True
        from_attributes=True
        
        