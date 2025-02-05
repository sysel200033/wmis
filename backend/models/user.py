from datetime import datetime

from sqlalchemy import Column, VARCHAR, DATE, DateTime
from sqlalchemy.orm import relationship
from database.config import Base


# Create User class
class UserModels(Base):
    __tablename__ = "users"
    email = Column(VARCHAR, unique=True, primary_key=True)
    password = Column(VARCHAR)
    birthday = Column(DATE)
    phone_number = Column(VARCHAR, unique=True)
    create_time = Column(DateTime, default=datetime.utcnow())
    last_login = Column(DateTime, default=datetime.utcnow())

    folders = relationship('FolderUserModels', back_populates='user', cascade="all, delete, delete-orphan")

    def __repr__(self) -> str:
        return f"<UserModels(email={self.email}, password={self.password}, birthday={self.birthday})>"
