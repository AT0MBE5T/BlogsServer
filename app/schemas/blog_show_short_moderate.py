from datetime import datetime
from pydantic import BaseModel


class BlogShowShortModerate(BaseModel):
    id: int
    header: str
    text: dict
    author: str
    created_at: datetime
    category_name: str

    class Config:
        from_attributes = True