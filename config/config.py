from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr


class Settings(BaseSettings):
    SENDER_EMAIL: EmailStr
    SENDER_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int

    model_config = SettingsConfigDict(env_file=".env")
