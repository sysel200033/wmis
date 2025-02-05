from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from auth.action import get_current_user
from crud.folder import FolderCRUD
from crud.folder_user import FolderUserCRUD
from crud.file import FileCRUD
from crud.dependencies import get_folder_crud, get_folder_user_crud, get_file_crud
import schemas.user as user_schema
import schemas.folder as folder_schema
import schemas.folder_user as folder_user_schema
import schemas.file as file_schema
from models.folder_user import Status

router = APIRouter(prefix="/folders", tags=["folders"])


@router.get("")
async def get_folders_by_head(head_folder_id: int | None = None, current_user: user_schema.Base = Depends(get_current_user), db_folder: FolderCRUD = Depends(get_folder_crud), db_folder_user: FolderUserCRUD = Depends(get_folder_user_crud)):
    return await db_folder.get_folders_by_head(head_folder_id=head_folder_id, user_mail=current_user.email)

@router.post("")
async def create_folder(
    new_folder: folder_schema.Base, current_user: user_schema.Base = Depends(get_current_user), db_folder: FolderCRUD = Depends(get_folder_crud), db_file: FileCRUD = Depends(get_file_crud), db_folder_user: FolderUserCRUD = Depends(get_folder_user_crud)
):
    folder = await db_folder.create_folder(current_user, new_folder)
    file = file_schema.Base(content="", folder_id=folder.id)
    folder_user = folder_user_schema.Base(user_mail=current_user.email, folder_id=folder.id, status=Status.CREATOR)
    await db_file.create_file(file)
    await db_folder_user.create_folder_user(folder_user)
    return folder

@router.put("")
async def update_folder_name(
    folder_id: int,
    new_folder_name: str,
    current_user: user_schema.Base = Depends(get_current_user),
    db_folder: FolderCRUD = Depends(get_folder_crud), 
    db_folder_user: FolderUserCRUD = Depends(get_folder_user_crud)):
    user = await db_folder_user.get_folder_user(mail=current_user.email, folderid=folder_id)
    if(user is not None and (user.status == Status.ADMIN or user.status == Status.CREATOR or user.status == Status.WRITE)):
        return await db_folder.update_folder_name(folder_id=folder_id, new_folder_name=new_folder_name)
    else:
        return status.HTTP_401_UNAUTHORIZED

@router.delete("")
async def delete_folder(
    folder_id: int,
    current_user: user_schema.Base = Depends(get_current_user),
    db_folder: FolderCRUD = Depends(get_folder_crud), 
    db_folder_user: FolderUserCRUD = Depends(get_folder_user_crud)):
    user = await db_folder_user.get_folder_user(mail=current_user.email, folderid=folder_id)
    if(user is not None and (user.status == Status.ADMIN or user.status == Status.CREATOR or user.status == Status.WRITE)):
        return await db_folder.delete_folder(folder_id=folder_id)
    else:
        return status.HTTP_401_UNAUTHORIZED