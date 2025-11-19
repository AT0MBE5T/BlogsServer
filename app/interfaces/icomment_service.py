from abc import abstractmethod, ABC

from app.schemas import CommentRequestSchema


class ICommentService(ABC):

    @abstractmethod
    async def get_all_by_blog_id(self, blog_id: int):
        pass

    @abstractmethod
    async def create(self, comment_schema: CommentRequestSchema) -> int | None:
        pass