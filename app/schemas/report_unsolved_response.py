from datetime import datetime
from pydantic import BaseModel


class ReportUnsolvedResponseSchema(BaseModel):
    id: int
    reason: str
    created_at: datetime
    blog_name: str
    login: str

    class Config:
        from_attributes = True