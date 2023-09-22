from typing import Optional

from pydantic import Field, PostgresDsn, RedisDsn, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

""" https://docs.pydantic.dev/latest/usage/pydantic_settings/ """


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__"
    )

    debug: Optional[str] = ""

    bot_token: str
    bot_fsm_storage: str

    postgres_dsn: PostgresDsn
    postgres_sync_dsn: str
    redis_dsn: Optional[RedisDsn] = ""
    custom_bot_api: Optional[str] = None
    app_host: Optional[str] = "0.0.0.0"
    app_port: Optional[int] = 9000
    webhook_domain: Optional[str] = ""
    webhook_path: Optional[str] = ""
    super_admin_id: Optional[int] = 0
    github_token: Optional[str] = ""
    github_repo: Optional[str] = ""
    replicate_api_token: Optional[str] = ""
    chat_id: Optional[str] = ""

    open_weather_token: Optional[str] = ""
    weather_stack_token: Optional[str] = ""

    @validator("bot_fsm_storage")
    def validate_bot_fsm_storage(cls, v):
        if v not in ("memory", "redis"):
            raise ValueError(
                "Incorrect 'bot_fsm_storage' value. Must be one of: memory, redis"
            )
        return v

    @validator("redis_dsn")
    def validate_redis_dsn(cls, v, values):
        if values["bot_fsm_storage"] == "redis" and not v:
            raise ValueError("Redis DSN string is missing!")
        return v

    @validator("webhook_path")
    def validate_webhook_path(cls, v, values):
        if values["webhook_domain"] and not v:
            raise ValueError("Webhook path is missing!")
        return v

    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"
    #     env_nested_delimiter = "__"


# class WeatherConfig(BaseSettings):
#     model_config = SettingsConfigDict(
#         env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__"
#     )
#     open_weather_token: Optional[str] = ""
#     weather_stack_token: Optional[str] = ""


# class FullConfig(Config, WeatherConfig):
#     pass


# print(Config().model_dump())
config = Config()
