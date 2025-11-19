from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces import ICategoryRepository
from app.models import Category


class CategoryRepository(ICategoryRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = Category

    async def get_all(self) -> Sequence[Category]:
        stmt = (select(self.model))
        result = await self._session.execute(stmt)
        return result.scalars().all()