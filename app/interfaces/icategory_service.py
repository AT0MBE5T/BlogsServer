from abc import abstractmethod, ABC
from app.schemas import CategorySchema


class ICategoryService(ABC):
    @abstractmethod
    async def get_all(self) -> list[CategorySchema]:
        pass