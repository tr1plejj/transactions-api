from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.settings import settings

engine = create_async_engine(settings.database_url)

sessionmaker = async_sessionmaker(engine)
