# type: ignore
import asyncio

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from passlib.hash import bcrypt

from src.infrastructure.database.models import Base, User, Account, Admin
from src.settings import settings

DATABASE_URL = settings.database_url
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpass"
TEST_ADMIN_EMAIL = "admin@example.com"
TEST_ADMIN_PASSWORD = "adminpass"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def seed_data(engine):
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        q = await session.execute(select(User).where(User.email == TEST_USER_EMAIL))
        user = q.scalars().first()
        if not user:
            user = User(
                email=TEST_USER_EMAIL,
                full_name="Test User",
                hashed_password=hash_password(TEST_USER_PASSWORD),
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            print(f"Created user {user.email} id={user.id}")
        else:
            print(f"User exists {user.email} id={user.id}")

        q = await session.execute(select(Account).where(Account.user_id == user.id))
        account = q.scalars().first()
        if not account:
            account = Account(balance=0, user_id=user.id)
            session.add(account)
            await session.commit()
            await session.refresh(account)
            print(f"Created account id={account.id} for user id={user.id}")
        else:
            print(f"Account exists id={account.id} for user id={user.id} (balance={account.balance})")

        q = await session.execute(select(Admin).where(Admin.email == TEST_ADMIN_EMAIL))
        admin = q.scalars().first()
        if not admin:
            admin = Admin(
                email=TEST_ADMIN_EMAIL,
                full_name="Test Admin",
                hashed_password=hash_password(TEST_ADMIN_PASSWORD),
            )
            session.add(admin)
            await session.commit()
            await session.refresh(admin)
            print(f"Created admin {admin.email} id={admin.id}")
        else:
            print(f"Admin exists {admin.email} id={admin.id}")

async def main():
    engine = create_async_engine(DATABASE_URL, echo=False)
    await create_tables(engine)
    await seed_data(engine)
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
