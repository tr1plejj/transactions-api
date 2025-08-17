from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import auth_admin_wrapper
from src.exceptions import WrongCredentials
from src.factories import get_admin_service, get_user_service
from src.schemas.base import SPayload, SAccount, STransaction
from src.schemas.user_schemas import SUserAuth, SUserRegister, SUserUpdate, SUser
from src.services.admin_service import AdminService
from src.services.user_service import UserService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login")
async def login_admin(
    admin_credentials: SUserAuth,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
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
async def get_all_users(
    payload: Annotated[SPayload, Depends(auth_admin_wrapper)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> list[SUser]:
    return await user_service.get_all_users()


@router.get("/user_accounts/{user_id}")
async def get_all_user_accounts(
    payload: Annotated[SPayload, Depends(auth_admin_wrapper)],
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> list[SAccount]:
    return await user_service.get_all_accounts(user_id)


@router.get("/user_transactions/{user_id}")
async def get_all_user_transactions(
    payload: Annotated[SPayload, Depends(auth_admin_wrapper)],
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> list[STransaction]:
    return await user_service.get_all_transactions(user_id)


@router.delete("/user/{user_id}")
async def delete_user(
    payload: Annotated[SPayload, Depends(auth_admin_wrapper)],
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> dict[str, bool]:
    await user_service.delete_user(user_id)
    return {"success": True}


@router.post("/create_user")
async def create_new_user(
    payload: Annotated[SPayload, Depends(auth_admin_wrapper)],
    user_data: SUserRegister,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> dict[str, bool]:
    await user_service.register_user(user_data)
    return {"success": True}


@router.patch("/update_user/{user_id}")
async def update_user(
    payload: Annotated[SPayload, Depends(auth_admin_wrapper)],
    user_id: int,
    user_data: SUserUpdate,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> dict[str, bool]:
    await user_service.update_user(user_id, user_data)
    return {"success": True}
