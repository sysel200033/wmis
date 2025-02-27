from datetime import datetime

from sqlalchemy import Column, VARCHAR, DATE, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database.config import Base


class FolderModels(Base):
    __tablename__ = "folders"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    name = Column(VARCHAR)
    header_folder_id = Column(ForeignKey('folders.id'), nullable=True)

    head_folder = relationship('FolderModels', remote_side=[id], backref='subfolders', cascade="all, delete, delete-orphan", single_parent=True)
    users = relationship('FolderUserModels', back_populates='folder', cascade="all, delete, delete-orphan")
    files = relationship('FileModels', back_populates='folder', cascade="all, delete, delete-orphan")

    def __repr__(self) -> str:
        return f"<FolderModels(id={self.id}, name={self.name}, head_folder_id={self.header_folder_id})>"
