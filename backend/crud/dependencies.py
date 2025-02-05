from typing import Generator

from database.config import async_session
from crud.user import UserCRUD
from crud.file import FileCRUD
from crud.folder import FolderCRUD
from crud.folder_user import FolderUserCRUD


async def get_db() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield session


async def get_user_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield UserCRUD(session)

async def get_file_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield FileCRUD(session)

async def get_folder_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield FolderCRUD(session)

async def get_folder_user_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield FolderUserCRUD(session)
