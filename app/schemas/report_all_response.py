from datetime import datetime
from pydantic import BaseModel


class ReportAllResponseSchema(BaseModel):
    id: int
    reason: str
    created_at: datetime
    blog_name: str
    login: str
    solved_at: datetime | None
    solved_by: str
    status: str

    class Config:
        from_attributes = True