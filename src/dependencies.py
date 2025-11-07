from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.schemas.base import SPayload
from src.services.auth_service import AuthService

security = HTTPBearer()


@inject
def auth_user_wrapper(
    auth_service: FromDishka[AuthService],
    auth: HTTPAuthorizationCredentials = Security(security),
) -> SPayload:
    payload = auth_service.decode_access_token(auth.credentials)
    if payload["type"] != "user":
        raise HTTPException(status_code=403, detail="Forbidden")
    return SPayload.model_validate(payload)


@inject
def auth_admin_wrapper(
    auth_service: FromDishka[AuthService],
    auth: HTTPAuthorizationCredentials = Security(security),
) -> SPayload:
    payload = auth_service.decode_access_token(auth.credentials)
    if payload["type"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return SPayload.model_validate(payload)
