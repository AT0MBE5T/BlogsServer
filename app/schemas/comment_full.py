from datetime import datetime
from pydantic import BaseModel


class CommentFull(BaseModel):
    id: int
    text: str
    author: str
    date: datetime
    avatar: bytes

    class Config:
        from_attributes = True