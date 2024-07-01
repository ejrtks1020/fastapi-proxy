from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from functools import wraps

from common.settings import settings

postgres_url = settings.MARIADB_URL.unicode_string()

engine = create_async_engine(postgres_url, echo=True, future=True)

AsyncSessionFactory = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session

class AsyncSessionContext:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = AsyncSessionFactory()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        self.session = None


def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if "session" in kwargs:
            return await func(*args, **kwargs)

        else:
            async with AsyncSessionContext() as session:
                kwargs["session"] = session

            try:
                result = await func(*args, **kwargs)
                await session.commit()

            except Exception as e:
                await session.rollback()
                raise e

            return result

    return wrapper