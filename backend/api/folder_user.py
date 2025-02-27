from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from auth.action import get_current_user
from crud.folder import FolderCRUD
from crud.folder_user import FolderUserCRUD
from crud.dependencies import get_folder_crud, get_folder_user_crud
import schemas.user as user_schema
import schemas.folder as folder_schema
import schemas.folder_user as folder_user_schema
from models.folder_user import Status

router = APIRouter(prefix="/folder_users", tags=["folder_users"])

@router.post("")
async def create_folder_user(
    new_folder_user: folder_user_schema.Base, current_user: user_schema.Base = Depends(get_current_user), db: FolderUserCRUD = Depends(get_folder_user_crud)
):
    user = await db.get_folder_user(mail=current_user.email, folderid=new_folder_user.folder_id)
    if(user.status == Status.ADMIN or user.status == Status.CREATOR):
        return await db.create_folder_user(new_folder_user)
    else:
        return status.HTTP_401_UNAUTHORIZED
    
@router.get("")
async def get_folder_user(
    folder_id: int, current_user: user_schema.Base = Depends(get_current_user), db: FolderUserCRUD = Depends(get_folder_user_crud)
):
    return await db.get_folder_user(mail=current_user.email, folderid=folder_id)

@router.put("")
async def update_folder_user(
    mail: str,
    folder_id: int,
    status: Status,
    current_user: user_schema.Base = Depends(get_current_user), 
    db: FolderUserCRUD = Depends(get_folder_user_crud)):
    user = await db.get_folder_user(mail=current_user.email, folderid=folder_id)
    if(user.status == Status.ADMIN or user.status == Status.CREATOR):
        return await db.update_folder_user(mail=mail, folder_id=folder_id, status=status)
    else:
        return status.HTTP_401_UNAUTHORIZED

@router.delete("")
async def delete_folder_user(
    mail: str,
    folder_id: int,
    current_user: user_schema.Base = Depends(get_current_user), 
    db: FolderUserCRUD = Depends(get_folder_user_crud)):
    user = await db.get_folder_user(mail=current_user.email, folderid=folder_id)
    if(user.status == Status.ADMIN or user.status == Status.CREATOR):
        return await db.delete_folder_user(mail=mail, folder_id=folder_id)
    else:
        return status.HTTP_401_UNAUTHORIZED