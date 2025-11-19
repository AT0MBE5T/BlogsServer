from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.core import get_category_service
from app.services import CategoryService

category_router = APIRouter(tags=['Categories'], prefix='/categories')

@category_router.get('/get-all')
async def get_all(
        category_service: CategoryService = Depends(get_category_service)):
        categories = await category_service.get_all()
        if not any(categories):
            return JSONResponse("There's nothing to get", status_code=404)
        else:
            return categories