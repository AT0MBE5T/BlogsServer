from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.core import Base


class Comment(Base):
    __tablename__ = 't_commentary'

    id: int = Column(Integer, primary_key=True)
    blog_id: int = Column(Integer)
    user_id: int = Column(Integer)
    text: str = Column(String)
    created_at: datetime = Column(DateTime)