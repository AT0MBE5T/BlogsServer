from pydantic import BaseModel


class RatingRequestSetSchema(BaseModel):
    blog_id: int
    user_id: int
    score: int

    class Config:
        from_attributes = True