from datetime import datetime
from pydantic import BaseModel

class RatingSchema(BaseModel):
    id: int
    blog_id: int
    user_id: int
    score: int
    created_at: datetime

    class Config:
        from_attributes = True