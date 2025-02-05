from datetime import date
from typing import Any
from pydantic import BaseModel
from .imports import folder

# File Schema

class Base(BaseModel):
    content: str
    folder_id: int

class Get(Base):
    file_id: int
    # folder: folder.Base
