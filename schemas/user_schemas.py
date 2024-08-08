from pydantic import BaseModel, constr, EmailStr, validator
import re
from typing import Optional
from schemas.user_roles_schema import UserRoleResponse
from utils.messages import (
    USER_NAME_MUST_CONTAIN_ONLY_LETTERS,
    USER_PASSWORD_MUST_BE_STRONG,
)


class UserCreate(BaseModel):
    first_name: constr(min_length=2, max_length=20)
    last_name: Optional[constr(min_length=2, max_length=20)] = None
    email: EmailStr
    password: constr(min_length=8)
    role_id: int

    @validator("first_name", "last_name")
    def name_must_contain_only_letters(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError(USER_NAME_MUST_CONTAIN_ONLY_LETTERS)
        return v.title()

    @validator("password")
    def password_must_be_strong(cls, v):
        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", v
        ):
            raise ValueError(USER_PASSWORD_MUST_BE_STRONG)
        return v


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    email: str
    role: UserRoleResponse

    class Config:
        from_attributes = True
        orm_mode = True
