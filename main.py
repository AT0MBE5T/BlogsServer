import uvicorn
from fastapi import FastAPI

from app.api.v1.endpoints.account import account_router
from app.api.v1.endpoints.blog import blog_router
from app.api.v1.endpoints.categories import category_router
from app.api.v1.endpoints.comment import comment_router
from app.api.v1.endpoints.rating import rating_router
from app.api.v1.endpoints.report import report_router
from app.core import setup_middlewares

app = FastAPI()

setup_middlewares(app)

app.include_router(account_router)
app.include_router(blog_router)
app.include_router(category_router)
app.include_router(comment_router)
app.include_router(rating_router)
app.include_router(report_router)

if __name__ == '__main__':
    uvicorn.run(app='main:app', host='localhost', port=7000, reload=True)