from datetime import datetime
from sqlalchemy import Column, VARCHAR, Integer, DATE, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database.config import Base
import enum

class Status(enum.Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    CREATOR = "creator"

class FolderUserModels(Base):
    __tablename__ = "folder_users"
    user_mail = Column(VARCHAR, ForeignKey('users.email'), primary_key=True)
    folder_id = Column(Integer, ForeignKey('folders.id'), primary_key=True)
    status = Column(Enum(Status), default=Status.READ)

    user = relationship('UserModels', back_populates='folders')
    folder = relationship('FolderModels', back_populates='users')

    def __repr__(self) -> str:
        return f"<FolderUserModels(user_mail={self.user_mail}, folder_id={self.folder_id}, status={self.status}, user={self.user}, folder={self.folder})>"
