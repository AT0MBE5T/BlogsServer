from fastapi import APIRouter, Depends

from app.core import get_current_user_safe, get_rating_service
from app.schemas import BlogConfirmation, RatingRequestSchema, RatingRequestSetSchema
from app.services import RatingService

rating_router = APIRouter(tags=['Ratings'], prefix='/ratings')

@rating_router.post('/get-avg-score-by-blog-id')
async def get_avg_score_by_blog_id(
        blog: BlogConfirmation,
        rating_service: RatingService = Depends(get_rating_service)):
        avg_rating = await rating_service.get_avg_score_by_blog_id(blog.blog_id)
        return avg_rating

@rating_router.post('/get-score-by-blog-user-id')
async def get_score_by_blog_user_id(request: RatingRequestSchema, rating_service: RatingService = Depends(get_rating_service), current_user=Depends(get_current_user_safe)):
    score = await rating_service.get_score_by_blog_user_id(request.blog_id, request.user_id)
    return score

@rating_router.post('/set-score')
async def set_score(request: RatingRequestSetSchema, rating_service: RatingService = Depends(get_rating_service), current_user=Depends(get_current_user_safe)):
    res = await rating_service.set_score(request.blog_id, request.user_id, request.score)
    return res
