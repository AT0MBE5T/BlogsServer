from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RejectSchema(BaseModel):
    header: str
    created_by: int
    created_at: datetime
    rejected_by: int
    rejected_at: datetime
    published_at: Optional[datetime]
    category_id: int

    class Config:
        from_attributes = True