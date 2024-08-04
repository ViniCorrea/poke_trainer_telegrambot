from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    CAPTURE_SUCCESS_RATE: float = 0.5
    FIND_POKEMON_RATE: float = 0.5
    WAIT_TIME_TO_CAPTURE: int = 3
    WAIT_TIME_TO_FIND_A_POKEMON: int = 3
    MAX_POKEMON_ID: int = 898
    PUBLIC_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
