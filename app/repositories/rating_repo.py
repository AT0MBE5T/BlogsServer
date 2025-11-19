from sqlalchemy import select, func, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces import IRatingRepository
from app.models import Rating


class RatingRepository(IRatingRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = Rating

    async def get_score_by_blog_user_id(self, blog_id: int, user_id: int) -> Rating:
        stmt = select(self.model.score).where(and_(self.model.blog_id == blog_id, self.model.user_id == user_id))
        result = await self._session.execute(stmt)
        return  result.scalar_one_or_none()

    async def get_avg_score_by_blog_id(self, blog_id: int) -> Rating:
        stmt = select(func.avg(self.model.score)).where(self.model.blog_id == blog_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def insert(self, rating: Rating):
        try:
            self._session.add(rating)
            await self._session.commit()
            await self._session.refresh(rating)
            return rating.id
        except Exception:
            await self._session.rollback()
            return None

    async def update(self, user_id: int, blog_id: int, rating: Rating):
        try:
            stmt = (
                update(Rating)
                .where(and_(Rating.user_id == user_id, Rating.blog_id == blog_id))
                .values({'score': rating.score})
            )

            result = await self._session.execute(stmt)

            await self._session.commit()

            if result.rowcount > 0:
                return True
            else:
                return None

        except Exception as ex:
            await self._session.rollback()
            return None