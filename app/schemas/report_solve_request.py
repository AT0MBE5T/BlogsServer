from pydantic import BaseModel


class ReportSolveRequestSchema(BaseModel):
    report_id: int
    user_id: int

    class Config:
        from_attributes = True