from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from auth.action import get_current_user
from crud.user import UserCRUD
from crud.dependencies import get_user_crud
import schemas.user as user_schema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[user_schema.Base])
async def get_users(db: UserCRUD = Depends(get_user_crud)):
    return await db.get_users()


@router.post("")
async def register(
    new_user: user_schema.Register, db: UserCRUD = Depends(get_user_crud)
):
    db_user = await db.get_user_by_email(email=new_user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    await db.create_user(new_user)
    return status.HTTP_201_CREATED


@router.delete("")
async def delete_user(
    current_user: user_schema.Base = Depends(get_current_user),
    db: UserCRUD = Depends(get_user_crud),
):
    return await db.delete_user(email=current_user.email)


@router.put("/password")
async def update_password(
    request: user_schema.Password,
    current_user: user_schema.Base = Depends(get_current_user),
    db: UserCRUD = Depends(get_user_crud),
):
    return await db.update_password(  email=current_user.email , password=request.password )

