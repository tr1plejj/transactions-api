from fastapi import Depends
from passlib.context import CryptContext

from src.services.admin_service import AdminService
from src.services.auth_service import AuthService
from src.services.transaction_service import TransactionService
from src.services.user_service import UserService
from src.uow import AbstractUnitOfWork, get_uow


def get_auth_service() -> AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return AuthService(pwd_context)


def get_user_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(uow, auth_service)


def get_transaction_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> TransactionService:
    return TransactionService(uow)


def get_admin_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
    auth_service: AuthService = Depends(get_auth_service),
) -> AdminService:
    return AdminService(uow, auth_service)
