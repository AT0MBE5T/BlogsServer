from abc import ABC, abstractmethod


class IRatingService(ABC):

    @abstractmethod
    async def get_score_by_blog_user_id(self, blog_id: int, user_id: int):
        pass

    @abstractmethod
    async def get_avg_score_by_blog_id(self, blog_id: int):
        pass

    @abstractmethod
    async def set_score(self, blog_id: int, user_id: int, score: int):
        pass
