from typing import Optional
from pydantic import BaseModel


class RegisterSchema(BaseModel):
    login: str
    password: str
    name: str
    surname: str
    patronymic: Optional[str] = None
    short_description: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    file: bytes

    class Config:
        from_attributes = True