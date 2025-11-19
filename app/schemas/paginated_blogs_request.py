from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PaginatedBlogsRequest(BaseModel):
    page: int
    itemsPerPage: int
    search_text: Optional[str] = None
    categories: Optional[list[int]] = None
    sortby: int
    dateFrom: Optional[datetime] = None
    dateTo: Optional[datetime] = None

    class Config:
        from_attributes = True