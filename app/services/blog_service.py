import math
from datetime import datetime

from app.interfaces import IBlogService, IBlogRepository
from app.models import Blog, Reject
from app.schemas import BlogSchema, BlogShowShort, BlogShowShortModerate, BlogShowShortUser, BlogFullInfo
from app.services import AvatarService, AccountService, RatingService


class BlogService(IBlogService):

    def __init__(self, repository: IBlogRepository, avatar_service: AvatarService, user_service: AccountService, rating_service: RatingService):
        self._repository = repository
        self._avatar_service = avatar_service
        self._user_service = user_service
        self.rating_service = rating_service

    async def create(self, blog: BlogSchema) -> int | None:
        blog = Blog(
            header=blog.header,
            created_by=blog.created_by,
            text=blog.text,
            category_id=blog.category_id
        )
        blog_id = await self._repository.insert(blog)
        return blog_id

    async def get_paginated(self, page: int, itemsPerPage: int, search_text: str, categories: list[int],
                            orderby: int, dateFrom: datetime | None, dateTo: datetime | None) -> tuple[list[BlogShowShort], int]:
        data = await self._repository.get_all_paginated(page, itemsPerPage, search_text, categories, orderby, dateFrom, dateTo)
        total_pages = math.ceil(data['total'] / itemsPerPage)
        res = [BlogShowShort(
            id=i.id,
            header=i.header,
            text=i.text,
            author=f'{i.name} {i.surname}',
            date=i.published_at,
            avatar=i.avatar,
            category_name=i.category_name
        ) for i in data['items']]
        return res, total_pages

    async def get_paginated_to_confirm(self) -> list[BlogShowShortModerate]:
        blogs = await self._repository.get_moderate_paginated()
        res = [BlogShowShortModerate(
            id=i.id,
            header=i.header,
            text=i.text,
            author=f'{i.name} {i.surname}',
            created_at=i.created_at,
            category_name=i.category_name
        ) for i in blogs]
        return res

    async def get_blogs_by_user_id(self, user_id: int) -> list[BlogShowShortUser]:
        published = await self._repository.get_user_published_blogs(user_id)
        pending = await self._repository.get_user_non_published_blogs(user_id)
        rejected = await self._repository.get_user_rejected_blogs(user_id)
        res = [
            BlogShowShortUser(
                id=i.id,
                header=i.header,
                published_at=i.published_at,
                created_at=i.created_at,
                category_name=i.category_name,
                status=status
            )
            for items, status in [
                (published, 'Published'),
                (pending, 'Pending'),
                (rejected, 'Rejected')
            ]
            for i in items
        ]
        return res

    async def get_blogs_by_user_id_for_profile(self, user_id: int, blogs_cnt: int) -> list[BlogShowShort]:
        data = await self._repository.get_blogs_for_profile(user_id, blogs_cnt)
        res = [BlogShowShort(
            id=i.id,
            header=i.header,
            text=i.text,
            author=f'{i.name} {i.surname}',
            date=i.published_at,
            avatar=i.avatar,
            category_name=i.category_name
        ) for i in data]
        return res

    async def get_blog_full_info_by_id(self, blog_id: int):
        try:
            blog = await self._repository.get_blog_by_id(blog_id)
            # if blog.published_at is None:
            #     return None
            user_id = blog.created_by
            user_data = await self._user_service.get_user_data_for_full_blog_info(blog.created_by)
            user_avatar = await self._avatar_service.get_avatar_by_user_id(blog.created_by)
            blog_avg_score = await self.rating_service.get_avg_score_by_blog_id(blog_id)
            user_score = await self.rating_service.get_score_by_blog_user_id(blog_id, user_id)
            res = BlogFullInfo(
                header=blog.header,
                text=blog.text,
                views_cnt=blog.views,
                author_name=f'{user_data.name} {user_data.surname}',
                user_description=user_data.short_description,
                date=blog.published_at,
                avatar=user_avatar,
                blog_avg_score=0 if blog_avg_score is None else blog_avg_score,
                user_score=0 if user_score is None else user_score
            )
            return res
        except Exception as ex:
            print(ex)
            return None

    async def increment_views(self, blog_id: int) -> bool:
        try:
            await self._repository.increment_view(blog_id)
            return True
        except Exception:
            return False

    async def publish_blog(self, blog_id) -> bool:
        try:
            await self._repository.update_publish_date(blog_id, datetime.now())
            return True
        except Exception:
            return False

    async def reject_blog(self, blog_id: int, user_id: int) -> bool:
        try:
            blog = await self._repository.get_blog_by_id(blog_id)
            reject = Reject(
                header=blog.header,
                created_by=blog.created_by,
                created_at=blog.created_at,
                rejected_by=user_id,
                rejected_at=datetime.now(),
                published_at=blog.published_at,
                category_id=blog.category_id,
            )
            await self._repository.insert_reject(reject)
            await self._repository.delete_blog(blog_id)
            return True
        except Exception:
            return False



    async def get_top_five_categories_blogs(self):
        res = await self._repository.get_top_five_categories_blogs()
        return res

    async def get_top_five_blog_views_by_user_id(self, user_id: int):
        res = await self._repository.get_top_five_blog_views_by_user_id(user_id)
        return res

    async def get_top_five_category_scores_by_user_id(self, user_id: int):
        res = await self._repository.get_top_five_category_scores_by_user_id(user_id)
        return res

    async def get_top_five_category_views_by_user_id(self, user_id: int):
        res = await self._repository.get_top_five_category_views_by_user_id(user_id)
        return res

    async def get_top_five_commented_blogs_by_user_id(self, user_id: int):
        res = await self._repository.get_top_five_commented_blogs_by_user_id(user_id)
        return res

    async def get_top_five_reported_blogs(self):
        res = await self._repository.get_top_five_reported_blogs()
        return res

    async def get_top_five_reported_users(self):
        res = await self._repository.get_top_five_reported_users()
        return res

    async def get_top_five_blog_views(self):
        res = await self._repository.get_top_five_blog_views()
        return res

    async def get_top_five_blogs_users(self):
        res = await self._repository.get_top_five_blogs_users()
        return res

    async def get_top_five_category_scores(self):
        res = await self._repository.get_top_five_category_scores()
        return res

    async def get_top_five_category_views(self):
        res = await self._repository.get_top_five_category_views()
        return res

    async def get_top_five_rating_users(self):
        res = await self._repository.get_top_five_rating_users()
        return res

    async def get_top_five_commented_blogs(self):
        res = await self._repository.get_top_five_commented_blogs()
        return res