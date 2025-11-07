from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import auth_user_wrapper
from src.exceptions import EmailHasAlreadyTaken, WrongCredentials
from src.schemas.base import SPayload, SAccount, STransaction
from src.schemas.user_schemas import SUserRegister, SUserAuth
from src.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register")
@inject
async def register_user(
    user: SUserRegister, user_service: FromDishka[UserService]
) -> dict[str, bool]:
    try:
        await user_service.register_user(user)
        return {"success": True}
    except EmailHasAlreadyTaken:
        raise HTTPException(
            status_code=403, detail="Email already is in use, choose another one"
        )


@router.post("/login")
@inject
async def login_user(
    user_credentials: SUserAuth,
    user_service: FromDishka[UserService],
) -> dict[str, str]:
    try:
        token = await user_service.login_user(user_credentials)
        return {"access_token": token}
    except WrongCredentials:
        raise HTTPException(status_code=403, detail="Wrong credentials")


@router.get("/me")
async def get_user_me(payload: Annotated[SPayload, Depends(auth_user_wrapper)]):
    return payload


@router.get("/accounts")
@inject
async def get_user_accounts(
    payload: Annotated[SPayload, Depends(auth_user_wrapper)],
    user_service: FromDishka[UserService],
) -> list[SAccount]:
    return await user_service.get_all_accounts(payload.user_id)


@router.get("/transactions")
@inject
async def get_user_transactions(
    payload: Annotated[SPayload, Depends(auth_user_wrapper)],
    user_service: FromDishka[UserService],
) -> list[STransaction]:
    return await user_service.get_all_transactions(payload.user_id)
