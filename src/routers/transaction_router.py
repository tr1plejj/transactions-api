from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.exceptions import InvalidSignature, TransactionAlreadyHandled
from src.factories import get_transaction_service
from src.schemas.base import STransaction
from src.services.transaction_service import TransactionService

router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post("/webhook")
async def handle_webhook_transaction(
    transaction: STransaction,
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
):
    try:
        await transaction_service.handle_transaction(transaction)
    except InvalidSignature:
        raise HTTPException(status_code=403, detail="Invalid signature")
    except TransactionAlreadyHandled:
        raise HTTPException(status_code=403, detail="Transaction already was handled")
