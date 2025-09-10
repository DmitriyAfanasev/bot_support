import logging

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingSettings(BaseModel):
    log_level: int = logging.INFO
    log_format: str = (
        "[%(asctime)s] | "
        "%(name)-20s | "
        "%(levelname)-8s | "
        "%(message)s (%(filename)s:%(lineno)d)"
    )
    datefmt: str = "%Y-%m-%d %H:%M:%S"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
    )
    bot_token: SecretStr
    logging: LoggingSettings = LoggingSettings()

    support_url: str = "https://t.me/@Sheldon_Kuper1"


settings = Settings()
