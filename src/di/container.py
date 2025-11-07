from dishka import AsyncContainer, make_async_container
from src.di.providers.database import DatabaseProvider
from src.di.providers.services import ServicesProvider


def container_factory() -> AsyncContainer:
    return make_async_container(DatabaseProvider(), ServicesProvider())
