from datetime import datetime
from fastapi import status
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from auth.utils import get_password_hash
from models.folder_user import FolderUserModels, Status
import schemas.file as file_schema
import schemas.folder_user as folder_user_schema
import schemas.user as user_schema


class FolderUserCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def get_folder_user(self, mail: str, folderid: int):
        stmt = select(FolderUserModels).where(FolderUserModels.user_mail == mail, FolderUserModels.folder_id == folderid).options(joinedload(FolderUserModels.folder))
        result = await self.db_session.execute(stmt)
        folder_user = result.scalars().first()
        return folder_user

    async def create_folder_user(self, folder_user: folder_user_schema.Base) -> folder_user_schema.Base:
        db_folder_user = FolderUserModels(
            user_mail=folder_user.user_mail,
            folder_id=folder_user.folder_id,
            status=folder_user.status
        )
        self.db_session.add(db_folder_user)
        await self.db_session.commit()
        return db_folder_user

    async def update_folder_user(self, mail: str, folder_id: int, status: Status):
        db_folder_user = await self.get_folder_user(mail, folder_id)
        stmt = (
            update(FolderUserModels)
            .where(FolderUserModels.user_mail == mail, FolderUserModels.folder_id == folder_id)
            .values(status=status)
        )
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)
        return db_folder_user    
    
    async def delete_folder_user(self, mail: str, folder_id: int):
        stmt = delete(FolderUserModels).where(FolderUserModels.user_mail == mail, FolderUserModels.folder_id == folder_id)
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)