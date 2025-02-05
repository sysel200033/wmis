from datetime import date
from typing import TYPE_CHECKING
from pydantic import BaseModel

# Folder schema

if TYPE_CHECKING:
    from .file import Base as FileBase
    from .user import Base as UserBase

class Base(BaseModel):
    name: str
    head_folder_id: int | None = None

class Get(Base):
    id: int
    users: 'UserBase'
    files: 'FileBase'
