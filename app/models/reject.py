from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String
from app.core import Base


class Reject(Base):
    __tablename__ = 't_reject'

    id: int = Column(Integer, primary_key=True)
    header: str = Column(String)
    created_by: int = Column(Integer)
    created_at: datetime = Column(DateTime)
    rejected_by: int = Column(Integer)
    rejected_at: datetime = Column(DateTime)
    published_at: datetime = Column(DateTime)
    category_id: int = Column(Integer)