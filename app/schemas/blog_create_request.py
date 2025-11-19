from pydantic import BaseModel


class BlogCreateRequest(BaseModel):
    header: str
    text: dict
    user_id: int
    category_id: int