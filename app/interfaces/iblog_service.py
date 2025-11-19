from abc import abstractmethod, ABC
from datetime import datetime

from app.schemas import BlogShowShortUser
from app.schemas import BlogSchema
from app.schemas import BlogShowShort
from app.schemas import BlogShowShortModerate


class IBlogService(ABC):
    @abstractmethod
    async def create(self, blog: BlogSchema) -> int | None:
        pass

    @abstractmethod
    async def get_paginated(self, page: int, itemsPerPage: int, search_text: str, categories: list[int], orderby: int, dateFrom: datetime, dateTo: datetime) -> tuple[list[BlogShowShort], int]:
        pass

    @abstractmethod
    async def get_blogs_by_user_id_for_profile(self, user_id: int, blogs_cnt: int) -> list[BlogShowShortUser]:
        pass

    @abstractmethod
    async def get_blog_full_info_by_id(self, blog_id: int):
        pass

    @abstractmethod
    async def get_paginated_to_confirm(self) -> list[BlogShowShortModerate]:
        pass

    @abstractmethod
    async def increment_views(self, blog_id: int) -> bool:
        pass

    @abstractmethod
    async def publish_blog(self, blog_id) -> bool:
        pass

    @abstractmethod
    async def reject_blog(self, blog_id: int, user_id: int) -> bool:
        pass

    @abstractmethod
    async def get_blogs_by_user_id(self, user_id: int) -> list[BlogShowShortUser]:
        pass

    @abstractmethod
    async def get_top_five_categories_blogs(self):
        pass

    @abstractmethod
    async def get_top_five_blog_views_by_user_id(self, user_id: int):
        pass

    @abstractmethod
    async def get_top_five_category_scores_by_user_id(self, user_id: int):
        pass

    @abstractmethod
    async def get_top_five_category_views_by_user_id(self, user_id: int):
        pass

    @abstractmethod
    async def get_top_five_commented_blogs_by_user_id(self, user_id: int):
        pass

    @abstractmethod
    async def get_top_five_reported_blogs(self):
        pass

    @abstractmethod
    async def get_top_five_reported_users(self):
        pass

    @abstractmethod
    async def get_top_five_blog_views(self):
        pass

    @abstractmethod
    async def get_top_five_blogs_users(self):
        pass

    @abstractmethod
    async def get_top_five_category_scores(self):
        pass

    @abstractmethod
    async def get_top_five_category_views(self):
        pass

    @abstractmethod
    async def get_top_five_rating_users(self):
        pass

    @abstractmethod
    async def get_top_five_commented_blogs(self):
        pass