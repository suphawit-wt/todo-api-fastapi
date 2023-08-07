import os

from sqlalchemy import URL

APP_ENV: str = os.getenv("APP_ENV", "development")

DB_HOST: str = os.getenv("DB_HOST", "localhost")
DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
DB_USER: str = os.getenv("DB_USERNAME", "")
DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
DB_NAME: str = os.getenv("DB_NAME", "todo_db")

DATABASE_URL: URL = URL.create(
    drivername="postgresql+asyncpg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

JWT_SECRET: str = os.getenv("JWT_SECRET", "")
JWT_ALGORITHM: str = "HS256"
JWT_ISSUER: str = os.getenv("JWT_ISSUER", "")
JWT_AUDIENCE: str = os.getenv("JWT_AUDIENCE", "")
