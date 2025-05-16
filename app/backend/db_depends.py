# install
from sqlalchemy.ext.asyncio import AsyncSession
# local
from app.backend.db import async_session_maker


async def get_db_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
