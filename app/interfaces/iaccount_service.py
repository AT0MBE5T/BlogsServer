from abc import ABC, abstractmethod
from app.schemas import AccountSchema


class IAccountService(ABC):
    @abstractmethod
    async def get_user_id(self, account: AccountSchema) -> int | None:
        pass

    @abstractmethod
    async def get_user_login(self, id: int) -> str | None:
        pass

    @abstractmethod
    async def get_name_by_user_id(self, user_id: int) -> str | None:
        pass

    @abstractmethod
    async def get_user_data_for_full_blog_info(self, user_id: int):
        pass

    @abstractmethod
    async def get_role_name_by_role_id(self, role_id: int) -> str:
        pass