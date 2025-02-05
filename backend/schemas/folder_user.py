from datetime import date
from typing import Any, TYPE_CHECKING
from pydantic import BaseModel
from models.folder_user import Status

if TYPE_CHECKING:
    from .folder import Base as FolderBase
    from .user import Base as UserBase

# File User Schema

class Base(BaseModel):
    user_mail: str
    folder_id: int
    status: Status

class Get(Base):
    user: 'UserBase'
    folder: 'FolderBase'
