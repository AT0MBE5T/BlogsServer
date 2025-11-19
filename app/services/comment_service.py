from datetime import datetime

from app.interfaces import ICommentService, ICommentRepository
from app.models import Comment
from app.schemas import CommentFull, CommentRequestSchema
from app.services import AvatarService, AccountService


class CommentService(ICommentService):

    def __init__(self, repository: ICommentRepository, avatar_service: AvatarService, user_service: AccountService):
        self._repository = repository
        self._avatar_service = avatar_service
        self._user_service = user_service

    async def get_all_by_blog_id(self, blog_id: int):
        comments = await self._repository.get_all_by_blog_id(blog_id)
        avatar_data = [await self._avatar_service.get_avatar_by_user_id(i.user_id) for i in comments]
        user_data = [await self._user_service.get_user_data_for_full_blog_info(i.user_id) for i in comments]
        res = [CommentFull(
            id=c.id,
            text=c.text,
            author=f'{u.name} {u.surname}',
            date=c.created_at,
            avatar=a
        ) for c,a,u in zip(comments, avatar_data, user_data)]
        return res

    async def create(self, comment_schema: CommentRequestSchema) -> int | None:
        comment = Comment(
            user_id=comment_schema.user_id,
            blog_id=comment_schema.blog_id,
            text=comment_schema.text,
            created_at=datetime.now()
        )
        comment_id = await self._repository.insert(comment)
        return comment_id