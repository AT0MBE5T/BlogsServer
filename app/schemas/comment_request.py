from pydantic import BaseModel

class CommentRequestSchema(BaseModel):
    blog_id: int
    user_id: int
    text: str

    class Config:
        from_attributes = True