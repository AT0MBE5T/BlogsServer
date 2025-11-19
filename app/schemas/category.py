from pydantic import BaseModel


class CategorySchema(BaseModel):
    key: int
    label: str

    class Config:
        from_attributes = True