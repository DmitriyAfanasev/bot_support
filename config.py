import logging
from pathlib import Path

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent

PATH_TO_IMAGES = BASE_DIR / "images"


class LoggingSettings(BaseModel):
    log_level: int = logging.WARNING
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
        extra="ignore",
    )
    bot_token: SecretStr
    logging: LoggingSettings = LoggingSettings()

    support_url: str | None
    support_contact_phone: str | None = None
    support_contact_first_name: str | None = None
    support_contact_last_name: str | None = None


settings = Settings()
