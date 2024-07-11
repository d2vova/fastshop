from typing import Optional, List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.authentication.security import get_password_hash
from src.common.databases.postgres import get_session
from src.common.repository.sqlalchemy import BaseSQLAlchemyRepository
from src.users.models.pydantic import (
    UserModel,
    UserWithPassword,
    UserAddressModel,
)
from src.users.models.sqlalchemy import User, UserAddress


class UserRepository(BaseSQLAlchemyRepository[User, UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, pydantic_model=UserModel, session=session)

    async def create_user(self, email: str, password: str, **kwargs) -> User:
        hashed_password = get_password_hash(password)
        user = User(email=email, hashed_password=hashed_password, **kwargs)
        self.session.add(user)
        await self.session.commit()
        return user

    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    async def get_by_email(self, email: str) -> Optional[UserWithPassword]:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            return None

        return UserWithPassword.model_validate(user)


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session=session)

class UserAddressRepository(BaseSQLAlchemyRepository[UserAddress, UserAddressModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=UserAddress, pydantic_model=UserAddressModel, session=session)

    async def get_by_user_id(self, user_id: int) -> Optional[UserAddressModel]:
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        addresses = result.scalars().all()
        return [self.pydantic_model.model_validate(address) for address in addresses]


def get_user_address_repository(session: AsyncSession = Depends(get_session)) -> UserAddressRepository:
    return UserAddressRepository(session=session)