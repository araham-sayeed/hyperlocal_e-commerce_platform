from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Hyperlocal API"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    database_url: str = "sqlite:///./hyperlocal.db"

    jwt_secret_key: str = "change-me-in-production-use-openssl-rand"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    otp_length: int = 6
    otp_ttl_seconds: int = 300
    otp_dev_fixed_code: str | None = "424242"

    default_search_radius_km: float = 15.0


@lru_cache
def get_settings() -> Settings:
    return Settings()
