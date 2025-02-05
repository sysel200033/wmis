from datetime import datetime

from sqlalchemy import Column, VARCHAR, DATE, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database.config import Base


class FileModels(Base):
    __tablename__ = "files"
    file_id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    content = Column(VARCHAR)
    folder_id = Column(Integer, ForeignKey('folders.id'))

    folder = relationship('FolderModels', back_populates='files')

    def __repr__(self) -> str:
        return f"<FileModels(file_id={self.file_id}, content={self.content}, folder_id={self.folder_id})>"
