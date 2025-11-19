from pydantic import BaseModel


class UserIdSchema(BaseModel):
    user_id: int

    class Config:
        from_attributes = True