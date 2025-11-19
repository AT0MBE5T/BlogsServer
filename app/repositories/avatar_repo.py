from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces import IAvatarRepository
from app.models import Avatar, Account


class AvatarRepository(IAvatarRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_file_by_id(self, avatar_id: int) -> int | None:
        res = await self._session.execute(
            select(Avatar.avatar).where(Avatar.id == avatar_id))
        return res.scalar_one_or_none()

    async def get_avatar_by_user_id(self, user_id: int) -> bytes | None:
        res = await self._session.execute(
            select(Avatar.avatar).join(Account, Account.avatar_id == Avatar.id).where(Account.id == user_id))
        return res.scalar_one_or_none()

    async def add_avatar(self, avatar: Avatar) -> int | None:
        try:
            self._session.add(avatar)
            await self._session.commit()
            await self._session.refresh(avatar)
            return avatar.id
        except Exception:
            await self._session.rollback()
            return None

    async def delete(self, id: int) -> bool:
        try:
            stmt = delete(Avatar).where(Avatar.id == id)
            await self._session.execute(stmt)
            await self._session.commit()
            return True
        except Exception:
            await self._session.rollback()
            return False