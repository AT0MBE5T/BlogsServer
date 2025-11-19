from sqlalchemy import Column, Integer, String
from app.core.database import Base
from app.schemas import AccountSchema


class Account(Base):
    __tablename__ = 't_user'

    id: int = Column(Integer, primary_key=True)
    login: str = Column(String)
    password: str = Column(String)
    name: str = Column(String)
    surname: str = Column(String)
    patronymic: str = Column(String)
    short_description: str = Column(String)
    phone_number: str = Column(String)
    email: str = Column(String)
    avatar_id: int = Column(Integer)
    role_id: int = Column(Integer)

    def to_read_model(self) -> AccountSchema:
        return AccountSchema(
            login = self.login,
            password = self.password,
            name = self.name,
            surname = self.surname,
            patronymic = self.patronymic,
            phone_number = self.phone_number,
            email = self.email,
            avatar_id=self.avatar_id,
            short_description=self.short_description,
            role_id=self.role_id
        )