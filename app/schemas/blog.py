from pydantic import BaseModel

class BlogSchema(BaseModel):
    header: str
    created_by: int
    text: dict
    category_id: int

    class Config:
        from_attributes = True