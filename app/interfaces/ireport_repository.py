from abc import ABC, abstractmethod

from app.models import Report


class IReportRepository(ABC):

    @abstractmethod
    async def get_unsolved(self):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def insert(self, report: Report):
        pass

    @abstractmethod
    async def delete(self, report_id: int, user_id: int):
        pass
