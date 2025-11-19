from .endpoints.account import account_router
from .endpoints.blog import blog_router
from .endpoints.categories import category_router
from .endpoints.rating import rating_router
from .endpoints.report import report_router
from .endpoints.comment import comment_router

__all__ = ['account_router', 'blog_router', 'category_router', 'comment_router', 'rating_router', 'report_router']
