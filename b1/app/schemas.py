from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr

class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    HR = "HR"
    STAFF = "STAFF"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleResponse(RoleBase):
    id: int

    class Config:
        from_attributes = True