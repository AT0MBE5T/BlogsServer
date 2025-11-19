from sqlalchemy import Column, Integer, BLOB
from app.core.database import Base
from app.schemas import AvatarSchema


class Avatar(Base):
    __tablename__ = 't_avatar'

    id: int = Column(Integer, primary_key=True)
    avatar: bytes = Column(BLOB)

    def to_read_model(self) -> AvatarSchema:
        return AvatarSchema(
            avatar = self.avatar
        )