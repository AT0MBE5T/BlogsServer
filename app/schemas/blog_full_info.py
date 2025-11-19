from datetime import datetime
from pydantic import BaseModel


class BlogFullInfo(BaseModel):
    header: str
    text: dict
    views_cnt: int
    author_name: str
    user_description: str
    date: datetime | None
    avatar: bytes
    blog_avg_score: float
    user_score: float

    class Config:
        from_attributes = True