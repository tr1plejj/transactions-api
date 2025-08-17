from src.exceptions import EmailHasAlreadyTaken, WrongCredentials
from src.schemas.base import SAccount, STransaction
from src.schemas.user_schemas import SUserRegister, SUserAuth, SUserUpdate, SUser
from src.services.auth_service import AuthService
from src.uow import AbstractUnitOfWork


class UserService:
    def __init__(self, uow: AbstractUnitOfWork, auth_service: AuthService) -> None:
        self.auth_service = auth_service
        self.uow = uow

    async def register_user(self, user: SUserRegister) -> None:
        if await self.uow.user_repository.check_if_email_in_db(str(user.email)):
            raise EmailHasAlreadyTaken
        hashed_password = self.auth_service.hash_password(user.password)
        await self.uow.user_repository.create_user(
            str(user.email), user.full_name, hashed_password
        )
        await self.uow.commit()

    async def login_user(self, user_credentials: SUserAuth) -> str:
        user = await self.uow.user_repository.get_by_email(str(user_credentials.email))
        if not user:
            raise WrongCredentials
        if not self.auth_service.authenticate_user(
            user_credentials.password, user.hashed_password
        ):
            raise WrongCredentials
        token = self.auth_service.encode_access_token(
            user.id, user.email, user.full_name, "user"
        )
        return token

    async def get_all_accounts(self, user_id: int) -> list[SAccount]:
        accounts = await self.uow.user_repository.get_all_accounts(user_id)
        return [SAccount.model_validate(account) for account in accounts]

    async def get_all_transactions(self, user_id: int) -> list[STransaction]:
        transactions = await self.uow.user_repository.get_all_transactions(user_id)
        return [
            STransaction.model_validate(transaction) for transaction in transactions
        ]

    async def get_all_users(self) -> list[SUser]:
        users = await self.uow.user_repository.get_all_users()
        return [SUser.model_validate(user) for user in users]

    async def delete_user(self, user_id) -> None:
        await self.uow.user_repository.delete_user(user_id)
        await self.uow.commit()

    async def update_user(self, user_id: int, user_data: SUserUpdate) -> None:
        user_dict = user_data.model_dump(exclude_unset=True)
        await self.uow.user_repository.update_user(user_id, user_dict)
        await self.uow.commit()
