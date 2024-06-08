import uuid
from typing import Optional, List

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    email: str
    username: str
    cutename: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    
    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    cutename: Optional[str]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    cutename: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
