from decimal import Decimal
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Algorithmic Trading Simulator"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/trading_simulator"
    secret_key: str = Field(
        default="local-development-secret-key-change-me",
        min_length=32,
    )
    access_token_expire_minutes: int = Field(default=30, gt=0)
    initial_wallet_balance: Decimal = Field(default=Decimal("100000.00"), ge=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
