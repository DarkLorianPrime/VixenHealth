from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from containers.vixenhealth_id.app.settings import settings

engine: AsyncEngine = create_async_engine(settings.database_url)
sessionmaker = async_sessionmaker(engine, class_=AsyncEngine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as sess:
        yield sess
