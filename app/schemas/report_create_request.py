from pydantic import BaseModel


class ReportCreateRequestSchema(BaseModel):
    user_id: int
    blog_id: int
    reason: str

    class Config:
        from_attributes = True