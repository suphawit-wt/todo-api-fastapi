from logging.config import fileConfig

from sqlalchemy import URL, Connection, pool, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from alembic import context
from todo_api.core.settings import DATABASE_URL
from todo_api.models.base import Base
from todo_api.models.todo import Todo  # noqa: F401
from todo_api.models.user import User  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


async def create_database_if_not_exists() -> None:
    engine: AsyncEngine = create_async_engine(
        URL.create(
            drivername=DATABASE_URL.drivername,
            username=DATABASE_URL.username,
            password=DATABASE_URL.password,
            host=DATABASE_URL.host,
            port=DATABASE_URL.port,
            database="postgres",
        ),
        poolclass=pool.NullPool,
        isolation_level="AUTOCOMMIT",
    )

    async with engine.connect() as connection:
        try:
            await connection.execute(text(f"CREATE DATABASE {DATABASE_URL.database}"))
            print(f"Database {DATABASE_URL.database} created successfully")
        except DBAPIError:
            print(
                f"Database {DATABASE_URL.database} already exists, skipping create database"
            )
        except Exception as e:
            print(f"Database error occur: {e}")
        finally:
            await connection.close()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable: AsyncEngine = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(create_database_if_not_exists())
    asyncio.run(run_migrations_online())
