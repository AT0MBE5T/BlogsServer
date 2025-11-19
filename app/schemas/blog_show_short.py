from datetime import datetime
from pydantic import BaseModel


class BlogShowShort(BaseModel):
    id: int
    header: str
    text: dict | None
    author: str
    date: datetime
    avatar: bytes
    category_name: str

    class Config:
        from_attributes = True