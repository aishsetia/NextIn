import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

path = os.path.abspath(os.environ.get("DOTENV_PATH", ".env"))
if os.path.exists(path):
    load_dotenv(dotenv_path=Path(__file__).parent / path)


class UvicornConfig(BaseSettings):
    PORT: int = 8080
    HOST: str = "0.0.0.0"

    WORKERS: int = 4
    RELOAD_ON_CHANGE: bool = False

    IS_CLOUD: bool = True

    class Config:
        env_prefix = "UVICORN_"


class DatabaseConfig(BaseSettings):
    HOST: str
    PORT: int = 5432

    USER: str
    PASSWORD: str

    NAME: str
    POOL_SIZE: int = 5

    class Config:
        env_prefix = "DB_"


class FirebaseConfig(BaseSettings):
    JWT_KEY: str
    API_KEY: str

    class Config:
        env_prefix = "FIREBASE_"


class OpenAIConfig(BaseSettings):
    API_KEY: str

    class Config:
        env_prefix = "OPENAI_"


class CONFIG:
    UVICORN = UvicornConfig()
    DB = DatabaseConfig()
    FIREBASE = FirebaseConfig()
    OPENAI = OpenAIConfig()