from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces import ICommentRepository
from app.models import Comment


class CommentRepository(ICommentRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = Comment

    async def get_all_by_blog_id(self, blog_id: int) -> list[Comment]:
        stmt = select(self.model).where(self.model.blog_id == blog_id).order_by(self.model.created_at.desc())
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def insert(self, comment: Comment) -> int | None:
        try:
            self._session.add(comment)
            await self._session.commit()
            await self._session.refresh(comment)
            return comment.id
        except Exception:
            await self._session.rollback()
            return None
