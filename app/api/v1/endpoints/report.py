from fastapi import APIRouter, Depends

from app.core import get_current_user_safe
from app.core import get_report_service
from app.schemas import ReportCreateRequestSchema, ReportSolveRequestSchema
from app.services import ReportService

report_router = APIRouter(tags=['Reports'], prefix='/reports')

@report_router.get('/get-unsolved-reports')
async def get_unsolved_reports(report_service: ReportService = Depends(get_report_service), current_user=Depends(get_current_user_safe)):
        reports = await report_service.get_all_unsolved()
        return reports

@report_router.get('/get-all-reports')
async def get_all_reports(report_service: ReportService = Depends(get_report_service), current_user=Depends(get_current_user_safe)):
        reports = await report_service.get_all()
        return reports

@report_router.post('/create-report')
async def create_report(request: ReportCreateRequestSchema, report_service: ReportService = Depends(get_report_service), current_user=Depends(get_current_user_safe)):
    res = await report_service.create_report(request)
    return res

@report_router.post('/solve-report')
async def solve_report(request: ReportSolveRequestSchema, report_service: ReportService = Depends(get_report_service), current_user=Depends(get_current_user_safe)):
    res = await report_service.solve_report(request)
    return res