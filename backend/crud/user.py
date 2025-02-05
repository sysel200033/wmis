from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from auth.utils import get_password_hash
from models.user import UserModels
import schemas.user as user_schema


class UserCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def get_user_by_email(self, email: str):
        stmt = select(UserModels).where(UserModels.email == email)
        result = await self.db_session.execute(stmt)
        user = result.scalars().first()
        return user

    async def get_users(self) -> List[user_schema.Base]:
        stmt = select(UserModels)
        result = await self.db_session.execute(stmt)
        users = result.scalars().all()
        return users

    async def create_user(self, user: user_schema.Register) -> user_schema.Base:
        db_user = UserModels(
            email=user.email,
            password=get_password_hash(user.password),
            birthday=user.birthday,
            phone_number=user.phone_number,
        )
        self.db_session.add(db_user)
        await self.db_session.commit()
        return db_user

    async def update_user_login(self, email: str):
        db_user = await self.get_user_by_email(email)
        db_user.last_login = datetime.utcnow()
        await self.db_session.refresh(db_user)
        return db_user

    async def update_birthday(self, email: str, birthday: datetime):
        stmt = (
            update(UserModels)
            .where(UserModels.email == email)
            .values(birthday=birthday)
        )
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)

    async def update_phone_number(self, email: str, number: str):
        stmt = (
            update(UserModels)
            .where(UserModels.email == email)
            .values(phone_number=number)
        )
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)

    async def update_password(self, email: str, password: str):
        stmt = (
            update(UserModels)
            .where(UserModels.email == email)
            .values(password=get_password_hash(password))
        )
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)

    async def delete_user(self, email: str):
        stmt = delete(UserModels).where(UserModels.email == email)
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)
