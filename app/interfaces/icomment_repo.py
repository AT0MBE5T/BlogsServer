from abc import ABC, abstractmethod
from app.models import Comment


class ICommentRepository(ABC):

    @abstractmethod
    async def get_all_by_blog_id(self, blog_id: int) -> list[Comment]:
        pass

    @abstractmethod
    async def insert(self, comment: Comment) -> int | None:
        pass