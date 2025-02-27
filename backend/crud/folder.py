from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from auth.utils import get_password_hash
from models.folder import FolderModels
from models.folder_user import FolderUserModels, Status
from models.file import FileModels
from models.user import UserModels
import schemas.folder as folder_schema
import schemas.user as user_schema
import schemas.file as file_schema
from sqlalchemy.sql import exists


class FolderCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def get_folders_by_head(self, head_folder_id: int | None, user_mail: str):
        stmt = select(FolderModels).where(FolderModels.header_folder_id == head_folder_id).filter(
        FolderModels.users.any(UserModels.email == user_mail)
    ).options(joinedload(FolderModels.files), joinedload(FolderModels.users))
        result = await self.db_session.execute(stmt)
        folders = result.unique().scalars().all()
        return folders
    
    async def get_folder_head(self, head_folder_name: str, folder_name: str):
        stmt = select(FolderModels).where(FolderModels.head_folder == head_folder_name, FolderModels.name == folder_name)
        result = await self.db_session.execute(stmt)
        folder = result.scalars().first()
        return folder
    
    async def get_folder_id(self, id: int):
        stmt = select(FolderModels).where(FolderModels.id == id)
        result = await self.db_session.execute(stmt)
        folder = result.scalars().first()
        return folder

    async def create_folder(self, current_user: user_schema.Base, folder: folder_schema.Base) -> folder_schema.Base:
        if(folder.head_folder_id is not None):
            db_folder = FolderModels(
                name=folder.name,
                head_folder_id=folder.head_folder_id
            )
        else:
            db_folder = FolderModels(
                name=folder.name
            )
        self.db_session.add(db_folder)
        await self.db_session.commit()
        return db_folder.id

    async def update_folder_name(self, folder_id: int, new_folder_name: str):
        db_folder = await self.get_folder_id(folder_id)
        stmt = (
            update(FolderModels)
            .where(FolderModels.id == folder_id)
            .values(name=new_folder_name)
        )
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)
        return db_folder
    
    async def delete_folder(self, folder_id: int):
        stmt = delete(FileModels).where(FileModels.folder_id == folder_id)
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)

        stmt = delete(FolderUserModels).where(FolderUserModels.folder_id == folder_id)
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)

        stmt = delete(FolderModels).where(FolderModels.id == folder_id)
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)