from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from app.core import get_db
from app.repositories import BlogRepository, ReportRepository
from app.repositories import AccountRepository
from app.repositories import AvatarRepository
from app.repositories import CategoryRepository
from app.repositories import CommentRepository
from app.repositories import RatingRepository
from app.services import AccountService, BlogService
from app.services import AvatarService
from app.services import CategoryService
from app.services import CommentService
from app.services import RatingService
from app.services import ReportService

Session = Annotated[AsyncSession, Depends(get_db)]

async def get_account_repo(session: AsyncSession = Depends(get_db)) -> AccountRepository:
    return AccountRepository(session)

def get_account_service(repo: AccountRepository = Depends(get_account_repo)) -> AccountService:
    return AccountService(repo)

async def get_avatar_repo(session: AsyncSession = Depends(get_db)) -> AvatarRepository:
    return AvatarRepository(session)

def get_avatar_service(repo: AvatarRepository = Depends(get_avatar_repo)) -> AvatarService:
    return AvatarService(repo)

async def get_rating_repo(session: AsyncSession = Depends(get_db)) -> RatingRepository:
    return RatingRepository(session)

def get_rating_service(repo: RatingRepository = Depends(get_rating_repo)) -> RatingService:
    return RatingService(repo)

async def get_blog_repo(session: AsyncSession = Depends(get_db)) -> BlogRepository:
    return BlogRepository(session)

def get_blog_service(repo: BlogRepository = Depends(get_blog_repo), avatar: AvatarService = Depends(get_avatar_service), account: AccountService = Depends(get_account_service), rating: RatingService = Depends(get_rating_service)) -> BlogService:
    return BlogService(repo, avatar, account, rating)

async def get_category_repo(session: AsyncSession = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(session)

def get_category_service(repo: CategoryRepository = Depends(get_category_repo)) -> CategoryService:
    return CategoryService(repo)

async def get_comment_repo(session: AsyncSession = Depends(get_db)) -> CommentRepository:
    return CommentRepository(session)

def get_comment_service(repo: CommentRepository = Depends(get_comment_repo), avatar: AvatarService = Depends(get_avatar_service), account: AccountService = Depends(get_account_service)) -> CommentService:
    return CommentService(repo, avatar, account)

async def get_report_repo(session: AsyncSession = Depends(get_db)) -> ReportRepository:
    return ReportRepository(session)

def get_report_service(repo: ReportRepository = Depends(get_report_repo)) -> ReportService:
    return ReportService(repo)