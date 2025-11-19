from pydantic import BaseModel


class AvatarSchema(BaseModel):
    avatar: bytes

    class Config:
        from_attributes = True