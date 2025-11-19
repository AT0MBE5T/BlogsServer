from abc import ABC, abstractmethod

from app.schemas import ReportSolveRequestSchema, ReportCreateRequestSchema


class IReportService(ABC):

    @abstractmethod
    async def get_all_unsolved(self):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def create_report(self, report: ReportCreateRequestSchema):
        pass

    @abstractmethod
    async def solve_report(self, report: ReportSolveRequestSchema):
        pass
