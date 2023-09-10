import secrets

from pydantic import AnyHttpUrl, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# from typing import Union


class Settings(BaseSettings):
    api_prefix: str = "/api/v1"
    secret_key: str = Field(secrets.token_urlsafe(32))
    backend_cors_origins: list[AnyHttpUrl] = []

    project_name: str
    pg_dsn: PostgresDsn

    # @validator("backend_cors_origins", pre=True)
    # def assemble_cors_origins(cls, v: Union[str, list[str]]) -> Union[list[str], str]:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )


settings = Settings()


if __name__ == "__main__":
    # print(settings)
    print(settings.model_dump())
