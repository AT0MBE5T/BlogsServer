from abc import ABC, abstractmethod

from app.models import Avatar


class IAvatarRepository(ABC):

    @abstractmethod
    async def get_file_by_id(self, avatar_id: int) -> int | None:
        pass

    @abstractmethod
    async def add_avatar(self, avatar: Avatar) -> int | None:
        pass

    @abstractmethod
    async def get_avatar_by_user_id(self, user_id: int) -> bytes | None:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass