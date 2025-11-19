from abc import ABC, abstractmethod
from typing import Tuple, Optional

from app.models import Account


class IAccountRepository(ABC):
    @abstractmethod
    async def get_user_id(self, login: str) -> int | None:
        raise NotImplemented

    @abstractmethod
    async def get_user_login(self, id: int) -> str | None:
        raise NotImplemented

    @abstractmethod
    async def register(self, account: Account):
        raise NotImplemented

    @abstractmethod
    async def get_password_hash_by_login(self, login: str):
        raise NotImplemented

    @abstractmethod
    async def get_name_by_user_id(self, user_id: int) -> Optional[Tuple[str, str]]:
        raise NotImplemented

    @abstractmethod
    async def get_data_for_blog(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    async def get_data_for_profile(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    async def get_role_name_by_role_id(self, role_id: int):
        pass