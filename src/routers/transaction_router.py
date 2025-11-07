from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException

from src.exceptions import InvalidSignature, TransactionAlreadyHandled
from src.schemas.base import STransaction
from src.services.transaction_service import TransactionService

router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post("/webhook")
@inject
async def handle_webhook_transaction(
    transaction: STransaction, transaction_service: FromDishka[TransactionService]
):
    try:
        await transaction_service.handle_transaction(transaction)
    except InvalidSignature:
        raise HTTPException(status_code=403, detail="Invalid signature")
    except TransactionAlreadyHandled:
        raise HTTPException(status_code=403, detail="Transaction already was handled")
