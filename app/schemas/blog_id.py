from pydantic import BaseModel


class BlogIdSchema(BaseModel):
    blog_id: int

    class Config:
        from_attributes = True