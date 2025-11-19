from pydantic import BaseModel


class BlogConfirmation(BaseModel):
    blog_id: int

    class Config:
        from_attributes = True