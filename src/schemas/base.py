from uuid import UUID

from pydantic import BaseModel, EmailStr


class SPayload(BaseModel):
    user_id: int
    email: EmailStr
    full_name: str


class STransaction(BaseModel):
    transaction_id: UUID
    account_id: int
    user_id: int
    amount: int
    signature: str

    class Config:
        from_attributes = True


class SAccount(BaseModel):
    id: int
    balance: int
    user_id: int

    class Config:
        from_attributes = True
