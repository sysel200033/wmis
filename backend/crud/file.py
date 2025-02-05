from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from auth.utils import get_password_hash
from models.file import FileModels
import schemas.file as file_schema
import schemas.user as user_schema


class FileCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def get_file_by_folder(self, folderid: int):
        stmt = select(FileModels).where(FileModels.folder_id == folderid)
        result = await self.db_session.execute(stmt)
        file = result.scalars().first()
        print(file)
        return file

    async def create_file(self, file: file_schema.Base) -> file_schema.Base:
        db_file = FileModels(
            content=file.content,
            folder_id=file.folder_id
        )
        self.db_session.add(db_file)
        await self.db_session.commit()
        return db_file

    async def update_file_content(self, folder_id: int, content: str):
        db_file = await self.get_file_by_folder(folderid=folder_id)
        stmt = (
            update(FileModels)
            .where(FileModels.folder_id == folder_id)
            .values(content=content)
        )
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)
        return db_file