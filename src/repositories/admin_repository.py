from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models import Admin


class AdminRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> Admin | None:
        query = select(Admin).filter_by(email=email)
        admin = await self.session.execute(query)
        return admin.scalar()
