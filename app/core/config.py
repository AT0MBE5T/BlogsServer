from datetime import timedelta

from authx import AuthX, AuthXConfig
from jwt import InvalidTokenError
from pydantic.v1 import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    ORIGINS: List[str]

    class Config:
        env_file = ".env"

settings = Settings(DATABASE_URL='mariadb+aiomysql://root:345543qwe@localhost:3306/db_blog', ORIGINS=["http://localhost:5173"])

config = AuthXConfig()
config.JWT_SECRET_KEY = "secret"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_COOKIE_NAME = "access-auth-token"
config.JWT_COOKIE_CSRF_PROTECT = False
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

security = AuthX(config=config)

from fastapi import HTTPException, status, Request
from authx.exceptions import MissingTokenError

async def get_current_user_safe(request: Request):
    try:
        return await security.access_token_required(request)
    except MissingTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authentication token.")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")

