from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from todo_api.core.settings import DATABASE_URL

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    pool_size=10,  # Number of connections to maintain in the pool
    max_overflow=20,  # Maximum number of connections allowed above `pool_size`
    pool_timeout=30,  # Maximum wait time (in seconds) for getting a connection
    pool_recycle=1800,  # Recycle connections after this number of seconds
    pool_pre_ping=True,  # Enable pool pre-ping to check connection health before use
)

AsyncDbSession: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)
