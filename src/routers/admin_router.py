from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import auth_admin_wrapper
from src.exceptions import WrongCredentials
from src.schemas.base import SPayload, SAccount, STransaction
from src.schemas.user_schemas import SUserAuth, SUserRegister, SUserUpdate, SUser
from src.services.admin_service import AdminService
from src.services.user_service import UserService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login")
@inject
async def login_admin(
    admin_credentials: SUserAuth,
    admin_service: FromDishka[AdminService],
) -> dict[str, str]:
    try:
        token = await admin_service.login_admin(admin_credentials)
        return {"access_token": token}
    except WrongCredentials:
        raise HTTPException(status_code=403, detail="Wrong credentials")


@router.get("/me")
async def get_admin_me(payload: Annotated[SPayload, Depends(auth_admin_wrapper)]):
    return payload


@router.get("/all_users")
@inject
async def get_all_users(
    payload: Annotated[SPayload, Depends(auth_admin_wrapper)],
    user_service: FromDishka[UserService],
) -> list[SUser]:
    return await user_service.get_all_users()


@router.get("/user_accounts/{user_id}")
@inject
async def get_all_user_accounts(
    payload: Annotated[SPayload, Depends(auth_admin_wrapper)],
    user_id: int,
    user_service: FromDishka[UserService],
) -> list[SAccount]:
    return await user_service.get_all_accounts(user_id)


@router.get("/user_transactions/{user_id}")
@inject
async def get_all_user_transactions(
    payload: Annotated[SPayload, Depends(auth_admin_wrapper)],
    user_id: int,
    user_service: FromDishka[UserService],
) -> list[STransaction]:
    return await user_service.get_all_transactions(user_id)


@router.delete("/user/{user_id}")
@inject
async def delete_user(
    payload: Annotated[SPayload, Depends(auth_admin_wrapper)],
    user_id: int,
    user_service: FromDishka[UserService],
) -> dict[str, bool]:
    await user_service.delete_user(user_id)
    return {"success": True}


@router.post("/create_user")
@inject
async def create_new_user(
    payload: Annotated[SPayload, Depends(auth_admin_wrapper)],
    user_data: SUserRegister,
    user_service: FromDishka[UserService],
) -> dict[str, bool]:
    await user_service.register_user(user_data)
    return {"success": True}


@router.patch("/update_user/{user_id}")
@inject
async def update_user(
    payload: Annotated[SPayload, Depends(auth_admin_wrapper)],
    user_id: int,
    user_data: SUserUpdate,
    user_service: FromDishka[UserService],
) -> dict[str, bool]:
    await user_service.update_user(user_id, user_data)
    return {"success": True}
