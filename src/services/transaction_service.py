import hashlib
import hmac

from src.broker.consumer import broker
from src.exceptions import TransactionAlreadyHandled
from src.schemas.base import STransaction
from src.settings import settings
from src.uow import AbstractUnitOfWork


class TransactionService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    @staticmethod
    def check_if_signature_valid(transaction: STransaction) -> bool:
        decoded_signature = f"{transaction.account_id}{transaction.amount}{transaction.transaction_id}{transaction.user_id}{settings.SECRET_KEY}"
        expected_signature = hashlib.sha256(
            decoded_signature.encode("utf-8")
        ).hexdigest()
        return hmac.compare_digest(expected_signature, transaction.signature)

    async def handle_transaction(self, transaction: STransaction) -> None:
        # if not self.check_if_signature_valid(transaction):
        #     raise InvalidSignature
        if await self.uow.transaction_repository.check_if_exists(
            transaction.transaction_id
        ):
            raise TransactionAlreadyHandled
        if not await self.uow.account_repository.check_if_exists(
            transaction.user_id, transaction.account_id
        ):
            await self.uow.account_repository.create_account(transaction.user_id)
        await self.uow.transaction_repository.create_transaction(
            transaction.user_id,
            transaction.account_id,
            transaction.amount,
            transaction.signature,
        )
        await self.uow.account_repository.update_balance(
            transaction.account_id, transaction.amount
        )
        await self.uow.commit()
        await broker.publish(transaction, "transaction")
