from datetime import datetime
from pydantic import BaseModel


class BlogShowShortUser(BaseModel):
    id: int
    header: str
    created_at: datetime
    published_at: datetime | None
    category_name: str
    status: str

    class Config:
        from_attributes = True