from abc import abstractmethod, ABC
from sqlalchemy import Sequence
from app.models import Category


class ICategoryRepository(ABC):
    @abstractmethod
    async def get_all(self) -> Sequence[Category]:
        pass