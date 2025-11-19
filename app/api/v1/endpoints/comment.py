import base64

from fastapi import APIRouter, Depends

from app.core import get_current_user_safe
from app.core import get_comment_service
from app.schemas import CommentRequestSchema
from app.schemas import BlogConfirmation
from app.services import CommentService

comment_router = APIRouter(tags=['Comments'], prefix='/comments')

@comment_router.post('/get-all-by-blog-id')
async def get_all_by_blog_id(
        blog: BlogConfirmation,
        comment_service: CommentService = Depends(get_comment_service), current_user=Depends(get_current_user_safe)):
        comments = await comment_service.get_all_by_blog_id(blog.blog_id)
        for comment in comments:
            if isinstance(comment.avatar, (bytes, bytearray)):
                comment.avatar = base64.b64encode(comment.avatar).decode('utf-8')
        return comments

@comment_router.post('/add-comment')
async def add_comment(request: CommentRequestSchema, comment_service: CommentService = Depends(get_comment_service), current_user=Depends(get_current_user_safe)):
    res = await comment_service.create(request)
    return res