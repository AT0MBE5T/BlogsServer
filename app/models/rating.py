from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from app.core import Base


class Rating(Base):
    __tablename__ = 't_rating'

    id: int = Column(Integer, primary_key=True)
    blog_id: int = Column(Integer)
    user_id: int = Column(Integer)
    score: int = Column(Integer)
    created_at: datetime = Column(DateTime)