from typing import Optional
from pydantic import BaseModel

class UserProfileSchema(BaseModel):
    login: str
    name: str
    surname: str
    patronymic: Optional[str] = None
    short_description: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    avatar: bytes
    role_id: int
    role_name: str

    class Config:
        from_attributes = True