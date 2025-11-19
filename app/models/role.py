from sqlalchemy import Column, Integer, String
from app.core import Base


class Role(Base):
    __tablename__ = 't_role'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)