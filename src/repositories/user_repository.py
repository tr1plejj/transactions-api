from datetime import datetime
from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models import User, Account, Transaction


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        query = select(User).filter_by(id=user_id)
        user = await self.session.execute(query)
        return user.scalar()

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).filter_by(email=email)
        user = await self.session.execute(query)
        return user.scalar()

    async def check_if_email_in_db(self, email: str) -> bool:
        query = select(User.email).filter_by(email=email)
        return bool(await self.session.scalar(query))

    async def create_user(
        self, email: str, full_name: str, hashed_password: str
    ) -> None:
        user = User(email=email, full_name=full_name, hashed_password=hashed_password)
        self.session.add(user)

    async def get_all_accounts(self, user_id: int) -> Sequence[Account]:
        query = select(Account).filter_by(user_id=user_id)
        accounts = await self.session.execute(query)
        return accounts.scalars().all()

    async def get_all_transactions(self, user_id: int) -> Sequence[Transaction]:
        query = select(Transaction).filter_by(user_id=user_id)
        transactions = await self.session.execute(query)
        return transactions.scalars().all()

    async def get_all_users(self) -> Sequence[User]:
        query = select(User)
        users = await self.session.execute(query)
        return users.scalars().all()

    async def delete_user(self, user_id: int) -> None:
        stmt = update(User).filter_by(id=user_id).values(deleted_at=datetime.now())
        await self.session.execute(stmt)

    async def update_user(self, user_id: int, user_data: dict) -> None:
        stmt = update(User).filter_by(id=user_id).values(**user_data)
        await self.session.execute(stmt)
