from datetime import datetime
from pydantic import BaseModel

class CommentSchema(BaseModel):
    id: int
    blog_id: int
    user_id: int
    text: str
    created_at: datetime

    class Config:
        from_attributes = True