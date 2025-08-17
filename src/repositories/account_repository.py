from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models import Account


class AccountRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def check_if_exists(self, user_id: int, account_id: int) -> bool:
        query = select(Account.id).filter_by(user_id=user_id, id=account_id)
        return bool(await self.session.scalar(query))

    async def create_account(self, user_id: int, balance: int = 0) -> None:
        account = Account(balance=balance, user_id=user_id)
        self.session.add(account)

    async def update_balance(self, account_id: int, amount: int) -> None:
        query = select(Account).filter_by(id=account_id).with_for_update()
        result = await self.session.execute(query)
        account = result.scalar()
        account.balance = account.balance + amount  # type: ignore
