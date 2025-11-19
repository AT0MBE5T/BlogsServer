from app.interfaces import ICategoryService, ICategoryRepository
from app.schemas import CategorySchema


class CategoryService(ICategoryService):

    def __init__(self, repository: ICategoryRepository):
        self._repository = repository

    async def get_all(self) -> list[CategorySchema]:
        categories = await self._repository.get_all()
        res = [CategorySchema(key=i.id, label=i.name) for i in categories]
        return res