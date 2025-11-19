from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON

from app.core.database import Base


class Blog(Base):
    __tablename__ = 't_blog'

    id: int = Column(Integer, primary_key=True)
    header: str = Column(String)
    created_at: datetime = Column(DateTime, default=datetime.now())
    created_by: int = Column(Integer)
    published_at: datetime = Column(DateTime, nullable=True)
    text: dict = Column(JSON)
    category_id: int = Column(Integer)
    views: int = Column(Integer, default=0)