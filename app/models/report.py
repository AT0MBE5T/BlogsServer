from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String
from app.core import Base


class Report(Base):
    __tablename__ = 't_report'

    id: int = Column(Integer, primary_key=True)
    blog_id: int = Column(Integer)
    created_by: int = Column(Integer)
    created_at: datetime = Column(DateTime)
    solved_by: int = Column(Integer)
    solved_at: datetime = Column(DateTime)
    reason: str = Column(String)