from abc import ABC, abstractmethod
from typing import Callable

from src.repositories.account_repository import AccountRepository
from src.repositories.admin_repository import AdminRepository
from src.repositories.transaction_repository import TransactionRepository
from src.repositories.user_repository import UserRepository


class AbstractUnitOfWork(ABC):
    user_repository: UserRepository
    admin_repository: AdminRepository
    account_repository: AccountRepository
    transaction_repository: TransactionRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: Callable):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.user_repository = UserRepository(self.session)
        self.admin_repository = AdminRepository(self.session)
        self.account_repository = AccountRepository(self.session)
        self.transaction_repository = TransactionRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
