from datetime import datetime

from app.interfaces import IReportService, IReportRepository
from app.models import Report
from app.schemas import ReportUnsolvedResponseSchema, ReportAllResponseSchema, ReportCreateRequestSchema, \
    ReportSolveRequestSchema


class ReportService(IReportService):

    def __init__(self, repository: IReportRepository):
        self._repository = repository

    async def get_all_unsolved(self):
        data = await self._repository.get_unsolved()
        res = [ReportUnsolvedResponseSchema(
            id=i.id,
            reason=i.reason,
            created_at=i.created_at,
            blog_name=i.blog_name,
            login=i.login
        ) for i in data]
        return res

    async def get_all(self):
        data = await self._repository.get_all()
        res = [ReportAllResponseSchema(
            id=i.id,
            reason=i.reason,
            created_at=i.created_at,
            blog_name=i.blog_name,
            login=i.login,
            solved_by=i.solved_by if i.solved_by is not None else '',
            solved_at=i.solved_at,
            status='Awaits' if i.solved_by is None else 'Solved'
        ) for i in data]
        return res

    async def create_report(self, report: ReportCreateRequestSchema):
        try:
            report = Report(
                blog_id=report.blog_id,
                created_by=report.user_id,
                created_at=datetime.now(),
                solved_by=None,
                solved_at=None,
                reason=report.reason
            )
            res = await self._repository.insert(report)
            return res
        except Exception as ex:
            return None


    async def solve_report(self, report: ReportSolveRequestSchema):
        try:
            res = await self._repository.delete(report.report_id, report.user_id)
            return True
        except Exception as ex:
            return False
