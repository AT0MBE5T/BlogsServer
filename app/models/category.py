from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Category(Base):
    __tablename__ = 't_category'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)