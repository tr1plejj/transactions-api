from dishka import Provider, provide, Scope
from passlib.context import CryptContext

from src.services.admin_service import AdminService
from src.services.auth_service import AuthService
from src.services.transaction_service import TransactionService
from src.services.user_service import UserService
from src.uow import AbstractUnitOfWork


class ServicesProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_pwd_context(self) -> CryptContext:
        return CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
        )

    @provide(scope=Scope.REQUEST)
    def provide_transaction_service(
        self, uow: AbstractUnitOfWork
    ) -> TransactionService:
        return TransactionService(uow)

    @provide(scope=Scope.REQUEST)
    def provide_auth_service(self, pwd_context: CryptContext) -> AuthService:
        return AuthService(pwd_context)

    @provide(scope=Scope.REQUEST)
    def provide_admin_service(
        self, uow: AbstractUnitOfWork, auth_service: AuthService
    ) -> AdminService:
        return AdminService(uow, auth_service)

    @provide(scope=Scope.REQUEST)
    def provide_user_service(self, uow: AbstractUnitOfWork, auth_service: AuthService) -> UserService:
        return UserService(uow, auth_service)
