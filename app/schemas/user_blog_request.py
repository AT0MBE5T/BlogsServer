from pydantic import BaseModel


class UserBlogRequestSchema(BaseModel):
    blog_id: int

    class Config:
        from_attributes = True