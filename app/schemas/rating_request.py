from pydantic import BaseModel


class RatingRequestSchema(BaseModel):
    blog_id: int
    user_id: int

    class Config:
        from_attributes = True