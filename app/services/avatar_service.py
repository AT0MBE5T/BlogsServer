from app.interfaces import IAvatarService, IAvatarRepository
from app.models import Avatar


class AvatarService(IAvatarService):

    def __init__(self, repository: IAvatarRepository):
        self._repository = repository

    async def get_avatar_by_id(self, avatar_id: int) -> bytes | None:
        avatar_blob = await self._repository.get_file_by_id(avatar_id)
        return avatar_blob

    async def get_avatar_by_user_id(self, user_id: int) -> bytes | None:
        avatar_bytes = await self._repository.get_avatar_by_user_id(user_id)
        return avatar_bytes

    async def add_avatar(self, avatar: bytes) -> int | None:
        new_avatar = Avatar(
            avatar=avatar
        )

        user_id = await self._repository.add_avatar(new_avatar)
        return user_id

    async def delete_avatar(self, avatar_id: int) -> bool:
        user_id = await self._repository.delete(avatar_id)
        return user_id
