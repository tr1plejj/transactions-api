from fastapi import Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.schemas.base import SPayload
from src.services.auth_service import AuthService

security = HTTPBearer()


def auth_user_wrapper(
    auth: HTTPAuthorizationCredentials = Security(security),
) -> SPayload:
    payload = AuthService.decode_access_token(auth.credentials)
    if payload["type"] != "user":
        raise HTTPException(status_code=403, detail="Forbidden")
    return SPayload.model_validate(payload)


def auth_admin_wrapper(
    auth: HTTPAuthorizationCredentials = Security(security),
) -> SPayload:
    payload = AuthService.decode_access_token(auth.credentials)
    if payload["type"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return SPayload.model_validate(payload)
