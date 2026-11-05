from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# The engine owns a pool of open connections, like mongoose.connect(). The server
# runs for a long time, so reusing connections is faster than opening new ones.
# It connects on first use, so the app can start while the database is down.
engine = create_async_engine(
    settings.app_database_url,
    # Neon suspends idle databases, which kills pooled connections. This tests a
    # connection before each use and replaces it if it has died.
    pool_pre_ping=True,
)

session_factory = async_sessionmaker(engine)


class Base(DeclarativeBase):
    """Every table class inherits from this, so Alembic can find them all."""


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency: a route asks for a session with `Depends(get_session)`.

    Code after `yield` runs once the response is done, so each request gets its
    own session and always hands its connection back to the pool.
    """
    async with session_factory() as session:
        yield session
