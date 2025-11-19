from abc import ABC, abstractmethod


class IAvatarService(ABC):
    @abstractmethod
    async def get_avatar_by_id(self, avatar_id: int) -> bytes | None:
        pass

    @abstractmethod
    async def add_avatar(self, avatar: bytes) -> int | None:
        pass

    @abstractmethod
    async def get_avatar_by_user_id(self, user_id: int) -> bytes | None:
        pass

    @abstractmethod
    async def delete_avatar(self, avatar_id: int) -> bool:
        pass