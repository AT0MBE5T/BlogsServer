import base64

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.core import get_current_user_safe
from app.core import get_blog_service
from app.schemas import UserBlogRequestSchema, UserIdSchema, BlogIdSchema, BlogCreateRequest
from app.schemas import BlogSchema
from app.schemas import BlogConfirmation
from app.schemas import PaginatedBlogsRequest
from app.services import BlogService

blog_router = APIRouter(tags=['Blogs'], prefix='/blogs')

@blog_router.post('/create', response_class=JSONResponse)
async def create(
        request: BlogCreateRequest,
        blog_service: BlogService = Depends(get_blog_service),
        current_user=Depends(get_current_user_safe)):
        blog_schema = BlogSchema(
            header=request.header,
            text=request.text,
            created_by=request.user_id,
            category_id=request.category_id
        )
        blog_id = await blog_service.create(blog_schema)
        if blog_id is None:
            return JSONResponse('Wrong credentials', status_code=404)
        else:
            return blog_id

@blog_router.post('/get-paginated')
async def get_paginated(
        request: PaginatedBlogsRequest,
        blog_service: BlogService = Depends(get_blog_service)):
        res, total_pages = await blog_service.get_paginated(request.page, request.itemsPerPage, request.search_text, request.categories, request.sortby, request.dateFrom, request.dateTo)
        for blog in res:
            if isinstance(blog.avatar, (bytes, bytearray)):
                blog.avatar = base64.b64encode(blog.avatar).decode('utf-8')
        return res, total_pages

@blog_router.post('/get-paginated-to-confirm')
async def get_paginated_to_confirm(blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
        res = await blog_service.get_paginated_to_confirm()
        return res

@blog_router.post('/get-user-blogs')
async def get_user_blogs_list(user: UserIdSchema, blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
        res = await blog_service.get_blogs_by_user_id(user.user_id)
        return res

@blog_router.post('/get-blog-full-info')
async def get_blog_full_info(blog: BlogIdSchema, blog_service: BlogService = Depends(get_blog_service)):
        res = await blog_service.get_blog_full_info_by_id(blog.blog_id)
        res.avatar = base64.b64encode(res.avatar).decode('utf-8')
        return res

@blog_router.post('/get-blogs-for-profile')
async def get_blogs_for_profile(user: UserIdSchema, blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
        res = await blog_service.get_blogs_by_user_id_for_profile(user.user_id, 5)
        for blog in res:
            if isinstance(blog.avatar, (bytes, bytearray)):
                blog.avatar = base64.b64encode(blog.avatar).decode('utf-8')
        return res

@blog_router.post('/increment-view', response_class=JSONResponse)
async def increment_view(blog: BlogConfirmation, blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.increment_views(blog.blog_id)
    if res:
        return JSONResponse('Success', status_code=200)
    else:
        return JSONResponse('Bad request', status_code=500)

@blog_router.post('/confirm-blog', response_class=JSONResponse)
async def confirm(blog: BlogConfirmation, blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.publish_blog(blog.blog_id)
    if res:
        return JSONResponse('Success', status_code=200)
    else:
        return JSONResponse('Bad request', status_code=500)

@blog_router.post('/reject-blog', response_class=JSONResponse)
async def reject(blog: UserBlogRequestSchema, blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.reject_blog(blog.blog_id, int(current_user.sub))
    if res:
        return JSONResponse('Success', status_code=200)
    else:
        return JSONResponse('Bad request', status_code=500)

@blog_router.post('/get-top-five-blog-views-by-user-id')
async def get_top_five_blog_views_by_user_id(user_id_schema: UserIdSchema, blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.get_top_five_blog_views_by_user_id(user_id_schema.user_id)
    return res

@blog_router.post('/get-top-five-category-scores-by-user-id')
async def get_top_five_category_scores_by_user_id(user_id_schema: UserIdSchema, blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.get_top_five_category_scores_by_user_id(user_id_schema.user_id)
    return res

@blog_router.post('/get-top-five-category-views-by-user-id')
async def get_top_five_category_views_by_user_id(user_id_schema: UserIdSchema, blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.get_top_five_category_views_by_user_id(user_id_schema.user_id)
    return res

@blog_router.post('/get-top-five-commented-blogs-by-user-id')
async def get_top_five_commented_blogs_by_user_id(user_id_schema: UserIdSchema, blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.get_top_five_commented_blogs_by_user_id(user_id_schema.user_id)
    return res

@blog_router.get('/get-top-five-categories-blogs')
async def get_top_five_categories_blogs(blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.get_top_five_categories_blogs()
    return res

@blog_router.get('/get-top-five-reported-blogs')
async def get_top_five_reported_blogs(blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.get_top_five_reported_blogs()
    return res

@blog_router.get('/get-top-five-reported-users')
async def get_top_five_reported_users(blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.get_top_five_reported_users()
    return res

@blog_router.get('/get-top-five-blog-views')
async def get_top_five_blog_views(blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.get_top_five_blog_views()
    return res

@blog_router.get('/get-top-five-blogs-users')
async def get_top_five_blogs_users(blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.get_top_five_blogs_users()
    return res

@blog_router.get('/get-top-five-category-scores')
async def get_top_five_category_scores(blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.get_top_five_category_scores()
    return res

@blog_router.get('/get-top-five-category-views')
async def get_top_five_category_views(blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.get_top_five_category_views()
    return res

@blog_router.get('/get-top-five-rating-users')
async def get_top_five_rating_users(blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.get_top_five_rating_users()
    return res

@blog_router.get('/get-top-five-commented-blogs')
async def get_top_five_commented_blogs(blog_service: BlogService = Depends(get_blog_service), current_user=Depends(get_current_user_safe)):
    res = await blog_service.get_top_five_commented_blogs()
    return res