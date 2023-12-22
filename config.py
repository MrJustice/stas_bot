from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    debug: bool = False


class TelegramBotConfig(BaseModel):
    token: str
    webhook_proxy_ngrok_domain: str
    parse_mode: str = "HTML"

    @property
    def webhook_path(self) -> str:
        return "/webhook"

    @property
    def webhook_url(self) -> str:
        return f"https://{self.TG_WEBHOOK_PROXY_NGROK_DOMAIN}{self.webhook_path}"


class Config(BaseSettings):
    """Project settings"""

    model_config = SettingsConfigDict(
        extra="allow", env_file=".env", env_file_encoding="utf-8", env_prefix="", env_nested_delimiter="__"
    )

    app: AppConfig = AppConfig()
    tg: TelegramBotConfig


@lru_cache()
def get_config() -> Config:
    return Config()
