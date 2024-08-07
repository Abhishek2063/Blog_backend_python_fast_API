from pydantic import BaseModel, constr, EmailStr, validator
import re
from typing import Optional
from schemas.user_roles_schema import UserRoleResponse


class UserCreate(BaseModel):
    first_name: constr(min_length=2, max_length=20)
    last_name: Optional[constr(min_length=2, max_length=20)]
    email: EmailStr
    password: constr(min_length=8)
    role_id: int

    @validator("first_name", "last_name")
    def name_must_contain_only_letters(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters")
        return v.title()

    @validator("password")
    def password_must_be_strong(cls, v):
        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", v
        ):
            raise ValueError(
                "Password must be at least 8 characters long and contain at least one letter, one number, and one special character"
            )
        return v


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    email: str
    role: UserRoleResponse

    class Config:
        orm_mode = True
