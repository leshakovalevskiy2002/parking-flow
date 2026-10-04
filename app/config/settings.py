from collections.abc import AsyncGenerator
from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models import Fine, ParkingPlace, ParkingSession, Rate, User  # noqa: F401
from app.models.base import Base


class DatabaseSettings(BaseSettings):
    user: str
    password: SecretStr
    db: str
    host: str = "localhost"
    port: int = 5432

    model_config = SettingsConfigDict(env_prefix="POSTGRES_", env_file=".env", extra="ignore")

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"


class JWTSettings(BaseSettings):
    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30

    model_config = SettingsConfigDict(env_prefix="JWT_", env_file=".env", extra="ignore")


@lru_cache
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


@lru_cache
def get_jwt_settings() -> JWTSettings:
    return JWTSettings()


jwt_settings = get_jwt_settings()
SECRET_KEY = jwt_settings.secret_key.get_secret_value()
ALGORITHM = jwt_settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = jwt_settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = jwt_settings.refresh_token_expire_days


database_settings = get_database_settings()
DATABASE_URL = database_settings.url
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
