from src.exceptions import WrongCredentials
from src.schemas.user_schemas import SUserAuth
from src.services.auth_service import AuthService
from src.uow import AbstractUnitOfWork


class AdminService:
    def __init__(self, uow: AbstractUnitOfWork, auth_service: AuthService) -> None:
        self.uow = uow
        self.auth_service = auth_service

    async def login_admin(self, admin_credentials: SUserAuth) -> str:
        admin = await self.uow.admin_repository.get_by_email(
            str(admin_credentials.email)
        )
        if not admin:
            raise WrongCredentials
        if not self.auth_service.authenticate_user(
            admin_credentials.password, admin.hashed_password
        ):
            raise WrongCredentials
        token = self.auth_service.encode_access_token(
            admin.id, admin.email, admin.full_name, "admin"
        )
        return token
