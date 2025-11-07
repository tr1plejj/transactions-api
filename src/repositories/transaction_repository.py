from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models import Transaction


class TransactionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def check_if_exists(self, transaction_id: UUID) -> bool:
        query = select(Transaction.transaction_id).filter_by(
            transaction_id=transaction_id
        )
        return bool(await self.session.scalar(query))

    async def create_transaction(
        self, user_id: int, account_id: int, amount: int, signature: str
    ) -> None:
        transaction = Transaction(
            user_id=user_id, account_id=account_id, amount=amount, signature=signature
        )
        self.session.add(transaction)
