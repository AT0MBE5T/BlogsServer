from typing import Optional

from pydantic import BaseModel

class AccountSchema(BaseModel):
    login: str
    password: str
    name: str
    surname: str
    patronymic: Optional[str] = ''
    short_description: str
    phone_number: Optional[str] = ''
    email: Optional[str] = ''
    avatar_id: int
    role_id: int

    class Config:
        from_attributes = True