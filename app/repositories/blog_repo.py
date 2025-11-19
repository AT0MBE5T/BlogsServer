from datetime import datetime

from sqlalchemy import select, and_, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces import IBlogRepository
from app.models import Blog, Account, Category, Avatar, Reject, Rating, Comment, Report


class BlogRepository(IBlogRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = Blog

    async def insert(self, blog: Blog) -> int | None:
        try:
            self._session.add(blog)
            await self._session.commit()
            await self._session.refresh(blog)
            return blog.id
        except Exception:
            await self._session.rollback()
            return None

    async def get_blog_by_id(self, blog_id: int):
        stmt = select(self.model).where(Blog.id == blog_id)
        res = await self._session.execute(stmt)
        return res.scalars().one()

    async def get_moderate_paginated(self):
        stmt = (select(Blog.id, Blog.header, Blog.text, Blog.created_at, Account.login, Account.name, Account.surname, Category.name.label('category_name'))
                .join(Account, Blog.created_by == Account.id)
                .join(Category, Category.id == Blog.category_id)
                .where(Blog.published_at.is_(None)))
        result = await self._session.execute(stmt)
        return result.all()

    async def get_all_paginated(
            self, page: int, itemsPerPage: int, search_text: str,
            categories: list[int], orderby: int, dateFrom: datetime, dateTo: datetime
    ):
        base_stmt = (
            select(Blog)
            .join(Account, Blog.created_by == Account.id)
            .join(Category, Category.id == Blog.category_id)
            .join(Avatar, Account.avatar_id == Avatar.id)
            .where(Blog.published_at.is_not(None))
        )

        if dateFrom:
            base_stmt = base_stmt.where(Blog.published_at >= dateFrom)
        if dateTo:
            base_stmt = base_stmt.where(Blog.published_at < dateTo)
        if search_text:
            base_stmt = base_stmt.where(Blog.header.like(f"%{search_text}%"))
        if categories:
            base_stmt = base_stmt.where(Blog.category_id.in_(categories))

        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total_count = await self._session.scalar(count_stmt)

        stmt = (
            select(
                Blog.id,
                Blog.header,
                Blog.text,
                Blog.published_at,
                Account.name,
                Account.surname,
                Avatar.avatar,
                Category.name.label('category_name'),
            )
            .join(Account, Blog.created_by == Account.id)
            .join(Category, Category.id == Blog.category_id)
            .join(Avatar, Account.avatar_id == Avatar.id)
            .where(Blog.published_at.is_not(None))
        )

        if dateFrom:
            stmt = stmt.where(Blog.published_at >= dateFrom)
        if dateTo:
            stmt = stmt.where(Blog.published_at < dateTo)
        if search_text:
            stmt = stmt.where(Blog.header.like(f"%{search_text}%"))
        if categories:
            stmt = stmt.where(Blog.category_id.in_(categories))

        if orderby == 0:
          stmt = stmt.order_by(Blog.views.desc())
        elif orderby == 1:
            stmt = stmt.order_by(Blog.published_at.desc())

        stmt = stmt.limit(itemsPerPage).offset((page - 1) * itemsPerPage)

        result = await self._session.execute(stmt)
        items = result.mappings().all()

        return {"total": total_count, "items": items}

    async def increment_view(self, blog_id: int):
        stmt = update(Blog).where(Blog.id == blog_id).values(views=Blog.views + 1)
        await self._session.execute(stmt)
        await self._session.commit()

    async def update_publish_date(self, blog_id: int, date: datetime):
        stmt = update(Blog).where(Blog.id == blog_id).values(published_at=date)
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_blog(self, blog_id: int):
        stmt = delete(Blog).where(Blog.id == blog_id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def insert_reject(self, reject: Reject):
        try:
            self._session.add(reject)
            await self._session.commit()
            await self._session.refresh(reject)
            return reject.id
        except Exception:
            await self._session.rollback()
            return None

    async def get_user_published_blogs(self, user_id: int):
        stmt = (select(Blog.id, Blog.header, Blog.created_at, Category.name.label('category_name'), Blog.published_at)
                .join(Account, Blog.created_by == Account.id)
                .join(Category, Category.id == Blog.category_id)
                .where(and_(Blog.published_at.is_not(None), Blog.created_by == user_id)))
        result = await self._session.execute(stmt)
        return result.all()

    async def get_user_non_published_blogs(self, user_id: int):
        stmt = (select(Blog.id, Blog.header, Blog.created_at, Blog.published_at, Category.name.label('category_name'))
                .join(Account, Blog.created_by == Account.id)
                .join(Category, Category.id == Blog.category_id)
                .where(and_(Blog.published_at.is_(None), Blog.created_by == user_id)))
        result = await self._session.execute(stmt)
        return result.all()

    async def get_user_rejected_blogs(self, user_id: int):
        stmt = (select(Reject.id, Reject.header, Reject.created_at, Reject.published_at, Category.name.label('category_name'))
                .join(Category, Category.id == Reject.category_id)
                .where(Reject.created_by == user_id))
        result = await self._session.execute(stmt)
        return result.all()



    async def get_blogs_for_profile(self, user_id: int, blogs_cnt: int):
        stmt = (
            select(
                Blog.id,
                Blog.header,
                Blog.text,
                Blog.published_at,
                Account.name,
                Account.surname,
                Avatar.avatar,
                Category.name.label('category_name'),
            )
            .join(Account, Blog.created_by == Account.id)
            .join(Category, Category.id == Blog.category_id)
            .join(Avatar, Account.avatar_id == Avatar.id)
            .limit(blogs_cnt)
            .where(and_(Blog.published_at.is_not(None), Account.id == user_id))
        )

        result = await self._session.execute(stmt)
        items = result.mappings().all()

        return items



    # user:
    # top 5 блогов по просмотрам
    async def get_top_five_blog_views_by_user_id(self, user_id: int):
        stmt = (select(func.concat(func.left(Blog.header, 35), '...').label('name'), Blog.views.label('value'))
                .join(Account, Blog.created_by == Account.id)
                .order_by(Blog.views.desc())
                .where(Blog.created_by == user_id).limit(5))
        result = await self._session.execute(stmt)
        return result.mappings().all()

    # top 5 разделов по оценкам
    async def get_top_five_category_scores_by_user_id(self, user_id: int):
        stmt = (select(Category.name.label('name'), func.sum(Rating.score).label('value'))
                .join(Blog, Blog.category_id == Category.id)
                .join(Rating, Rating.blog_id == Blog.id)
                .group_by(Category.name)
                .order_by(func.sum(Rating.score).desc())
                .where(Blog.created_by == user_id).limit(5))
        result = await self._session.execute(stmt)
        return result.mappings().all()

    # top 5 разделов по просмотрам
    async def get_top_five_category_views_by_user_id(self, user_id: int):
        stmt = (select(Category.name.label('name'), func.sum(Blog.views).label('value'))
                .join(Blog, Blog.category_id == Category.id)
                .group_by(Category.name)
                .order_by(func.sum(Blog.views).desc())
                .where(Blog.created_by == user_id).limit(5))
        result = await self._session.execute(stmt)
        return result.mappings().all()

    # top 5 блогов по комментариям
    async def get_top_five_commented_blogs_by_user_id(self, user_id: int):
        stmt = (select(func.concat(func.left(Blog.header, 35), '...').label('name'), func.count(Comment.id).label('value'))
                .join(Account, Blog.created_by == Account.id)
                .join(Comment, Comment.blog_id == self.model.id)
                .group_by(Blog.header)
                .order_by(func.count(Comment.id).desc())
                .where(Blog.created_by == user_id).limit(5))
        result = await self._session.execute(stmt)
        return result.mappings().all()

    # moder:
    # top 5 блогов по жалобам
    async def get_top_five_reported_blogs(self):
        stmt = (select(func.concat(func.left(Blog.header, 35), '...').label('name'), func.count(Blog.id).label('value'))
                .join(Report, Report.blog_id == Blog.id)
                .group_by(Blog.header)
                .order_by(func.count(Blog.id).desc()).limit(5))
        result = await self._session.execute(stmt)
        return result.mappings().all()

    # top 5 категория по кол-ву блогов
    async def get_top_five_categories_blogs(self):
        stmt = (select(Category.name, func.count(Blog.id).label('value'))
                .join(Blog, Blog.category_id == Category.id)
                .group_by(Category.name)
                .order_by(func.count(Blog.id).desc()).limit(5))
        result = await self._session.execute(stmt)
        return result.mappings().all()

    # top 5 пользователей по жалобам
    async def get_top_five_reported_users(self):
        stmt = (select(Account.login.label('name'), func.count(Blog.id).label('value'))
                .join(Blog, Blog.created_by == Account.id)
                .join(Report, Report.blog_id == Blog.id)
                .group_by(Account.login)
                .order_by(func.count(Blog.id).desc()).limit(5))
        result = await self._session.execute(stmt)
        return result.mappings().all()

    #top 5 блогов по просмотрам
    async def get_top_five_blog_views(self):
        stmt = (select(func.concat(func.left(Blog.header, 35), '...').label('name'), Blog.views.label('value'))
                .join(Account, Blog.created_by == Account.id)
                .order_by(Blog.views.desc()).limit(5))
        result = await self._session.execute(stmt)
        return result.mappings().all()

    #top 5 юзеров по кол-ву выложенных блогов
    async def get_top_five_blogs_users(self):
        stmt = (
            select(Account.login.label('name'), func.count(Blog.id).label("blog_count").label('value'))
            .join(Blog, Blog.created_by == Account.id)
            .group_by(Account.login)
            .order_by(func.count(Blog.id).desc())
            .limit(5)
        )
        result = await self._session.execute(stmt)
        return result.mappings().all()

    #top 5 разделов по оценкам
    async def get_top_five_category_scores(self):
        stmt = (select(Category.name.label('name'), func.sum(Rating.score).label('value'))
                .join(Blog, Blog.category_id == Category.id)
                .join(Rating, Rating.blog_id == Blog.id)
                .group_by(Category.name)
                .order_by(func.sum(Rating.score).desc()).limit(5))
        result = await self._session.execute(stmt)
        return result.mappings().all()

    # top 5 разделов по просмотрам
    async def get_top_five_category_views(self):
        stmt = (select(Category.name.label('name'), func.sum(Blog.views).label('value'))
                .join(Blog, Blog.category_id == Category.id)
                .group_by(Category.name)
                .order_by(func.sum(Blog.views).desc()).limit(5))
        result = await self._session.execute(stmt)
        return result.mappings().all()

    #top 5 юзеров по оценкам
    async def get_top_five_rating_users(self):
        stmt = (select(Account.login.label('name'), func.sum(Rating.score).label('value'))
                .join(Blog, Blog.created_by == Account.id)
                .join(Rating, Rating.blog_id == Blog.id)
                .group_by(Account.login)
                .order_by(func.sum(Rating.score).desc())
                .limit(5))
        result = await self._session.execute(stmt)
        return result.mappings().all()

    #top 5 блогов по комментариям
    async def get_top_five_commented_blogs(self):
        stmt = (select(func.concat(func.left(Blog.header, 35), '...').label('name'), func.count(Comment.id).label('value'))
                .join(Comment, Comment.blog_id == self.model.id)
                .group_by(Blog.header)
                .order_by(func.count(Comment.id).desc())
                .limit(5))
        result = await self._session.execute(stmt)
        return result.mappings().all()
