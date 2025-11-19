from typing import Optional, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces import IAccountRepository
from app.models import Account, Role


class AccountRepository(IAccountRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_id(self, login: str) -> int | None:
        res = await self._session.execute(
            select(Account.id).where(Account.login == login))
        return res.scalar_one_or_none()

    async def get_user_login(self, id: int) -> str | None:
        res = await self._session.execute(select(Account.login).where(Account.id == id))
        return res.scalar_one_or_none()

    async def get_password_hash_by_login(self, login: str):
        res = await self._session.execute(select(Account.password).where(Account.login == login))
        return res.scalar_one_or_none()

    async def register(self, account: Account):
        try:
            self._session.add(account)
            await self._session.commit()
            await self._session.refresh(account)
            return account.id
        except Exception:
            await self._session.rollback()
            return None

    async def get_name_by_user_id(self, user_id: int) -> Optional[Tuple[str, str]]:
        res = await self._session.execute(select(Account.name, Account.surname).where(Account.id == user_id))
        return res.one_or_none()

    async def get_data_for_blog(self, user_id: int):
        stmt = select(Account.name, Account.surname, Account.avatar_id, Account.short_description).where(Account.id == user_id)
        res = await self._session.execute(stmt)
        return res.one_or_none()

    async def get_data_for_profile(self, user_id: int):
        stmt = select(Account.login, Account.name, Account.surname, Account.patronymic, Account.short_description, Account.email, Account.phone_number, Account.role_id).where(Account.id == user_id)
        res = await self._session.execute(stmt)
        return res.one_or_none()

    async def get_role_name_by_role_id(self, role_id: int):
        stmt = select(Role.name).where(Role.id == role_id)
        res = await self._session.execute(stmt)
        return res.scalar()