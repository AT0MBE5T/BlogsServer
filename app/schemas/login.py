from pydantic import BaseModel

class LoginSchema(BaseModel):
    login: str
    password: str

    class Config:
        from_attributes = True