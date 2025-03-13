from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from auth.action import get_current_user
from crud.user import UserCRUD
from crud.file import FileCRUD
from crud.folder_user import FolderUserCRUD
from crud.dependencies import get_file_crud, get_folder_user_crud
import schemas.user as user_schema
import schemas.file as file_schema
from models.folder_user import Status

router = APIRouter(prefix="/files", tags=["files"])

@router.get("/{folder_id}", response_model=file_schema.Get)
async def get_file_folder(folder_id: int, current_user: user_schema.Base = Depends(get_current_user), db_file: FileCRUD = Depends(get_file_crud), db_folder_user: FolderUserCRUD = Depends(get_folder_user_crud)):
    user = await db_folder_user.get_folder_user(mail=current_user.email, folderid=folder_id)
    if(user):
        return await db_file.get_file_by_folder(folderid=folder_id)
    else:
        return status.HTTP_401_UNAUTHORIZED

@router.put("/{folder_id}")
async def update_file_content(
    content: str,
    folder_id: int,
    current_user: user_schema.Base = Depends(get_current_user),
    db_file: FileCRUD = Depends(get_file_crud),
    db_folder_user: FolderUserCRUD = Depends(get_folder_user_crud)
):
    user = await db_folder_user.get_folder_user(mail=current_user.email, folderid=folder_id)
    if(user.status == Status.ADMIN or user.status == Status.CREATOR or user.status == Status.WRITE):
        return await db_file.update_file_content(folder_id=folder_id, content=content)
    else:
        return status.HTTP_401_UNAUTHORIZED

