from abc import abstractmethod, ABC
from datetime import datetime

from app.models import Blog
from app.models import Reject


class IBlogRepository(ABC):
    @abstractmethod
    async def insert(self, blog: Blog) -> int | None:
        pass

    @abstractmethod
    async def get_all_paginated(self, page: int, itemsPerPage: int, search_text: str, categories: list[int], orderby: int, dateFrom: datetime, dateTo: datetime):
        pass

    @abstractmethod
    async def get_moderate_paginated(self):
        pass

    @abstractmethod
    async def get_blog_by_id(self, blog_id: int):
        pass

    @abstractmethod
    async def get_blogs_for_profile(self, user_id: int, blogs_cnt: int):
        pass

    @abstractmethod
    async def increment_view(self, blog_id: int):
        pass

    @abstractmethod
    async def update_publish_date(self, blog_id: int, date: datetime):
        pass

    @abstractmethod
    async def delete_blog(self, blog_id: int):
        pass

    @abstractmethod
    async def insert_reject(self, reject: Reject):
        pass

    @abstractmethod
    async def get_user_published_blogs(self, user_id: int):
        pass

    @abstractmethod
    async def get_user_non_published_blogs(self, user_id: int):
        pass

    @abstractmethod
    async def get_user_rejected_blogs(self, user_id: int):
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