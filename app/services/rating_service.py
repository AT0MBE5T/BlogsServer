from datetime import datetime

from app.interfaces import IRatingService, IRatingRepository
from app.models import Rating


class RatingService(IRatingService):

    def __init__(self, repository: IRatingRepository):
        self._repository = repository

    async def get_score_by_blog_user_id(self, blog_id: int, user_id: int):
        res = await self._repository.get_score_by_blog_user_id(blog_id, user_id)
        return res

    async def get_avg_score_by_blog_id(self, blog_id: int):
        res = await self._repository.get_avg_score_by_blog_id(blog_id)
        return res

    async def set_score(self, blog_id: int, user_id: int, score: int):
        try:
            score_data = await self._repository.get_score_by_blog_user_id(blog_id, user_id)
            rating = Rating(
                blog_id=blog_id,
                user_id=user_id,
                score=score,
                created_at=datetime.now()
            )
            if score_data is None:
                await self._repository.insert(rating)
                return True
            else:
                await self._repository.update(user_id, blog_id, rating)
                return True
        except Exception:
            return False
