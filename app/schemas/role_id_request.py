from pydantic import BaseModel


class RoleIdSchema(BaseModel):
    role_id: int

    class Config:
        from_attributes = True