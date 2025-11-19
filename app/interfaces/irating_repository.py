from abc import ABC, abstractmethod
from app.models import Rating


class IRatingRepository(ABC):

    @abstractmethod
    async def get_score_by_blog_user_id(self, blog_id: int, user_id: int) -> Rating:
        pass

    @abstractmethod
    async def get_avg_score_by_blog_id(self, blog_id: int) -> Rating:
        pass

    @abstractmethod
    async def insert(self, rating: Rating):
        pass

    @abstractmethod
    async def update(self, user_id: int, blog_id: int, rating: Rating):
        pass
