import secrets

from pydantic import AnyHttpUrl, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_prefix: str = "/api/v1"
    secret_key: str = Field(secrets.token_urlsafe(32))
    backend_cors_origins: list[AnyHttpUrl] = []

    project_name: str
    pg_dsn: PostgresDsn

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )


settings = Settings()  # type: ignore


if __name__ == "__main__":
    # print(settings)
    print(settings.model_dump())
