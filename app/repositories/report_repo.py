from datetime import datetime

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.interfaces import IReportRepository
from app.models import Report, Account, Blog


class ReportRepository(IReportRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = Report

    async def get_unsolved(self):
        stmt = (select(Report.id, Report.created_at, Report.reason, Blog.header.label('blog_name'), Account.login)
                .join(Account, Account.id == Report.created_by)
                .join(Blog, Blog.id == Report.blog_id)
                .where(Report.solved_at.is_(None)))
        result = await self._session.execute(stmt)
        return result.all()

    async def get_all(self):
        Creator = aliased(Account)
        Solver = aliased(Account)
        stmt = (select(Report.id, Report.created_at, Report.reason, Report.solved_at, Blog.header.label('blog_name'), Creator.login, Solver.login.label('solved_by'))
                .join(Blog, Blog.id == Report.blog_id)
                .join(Creator, Creator.id == Report.created_by)
                .join(Solver, Solver.id == Report.solved_by, isouter=True))
        result = await self._session.execute(stmt)
        return result.all()

    async def insert(self, report: Report):
        try:
            self._session.add(report)
            await self._session.commit()
            await self._session.refresh(report)
            return report.id
        except Exception:
            await self._session.rollback()
            return None

    async def delete(self, report_id: int, user_id: int):
        try:
            stmt = (
                update(Report)
                .where(and_(Report.id == report_id))
                .values(solved_by=user_id, solved_at=datetime.now())
            )
            await self._session.execute(stmt)
            await self._session.commit()
            return True
        except Exception as ex:
            await self._session.rollback()
            return None