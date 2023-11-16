# from pydantic_settings import BaseSettings
import os
from typing import ClassVar
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    ENV_TYPE: ClassVar[str] = os.getenv("ENV_TYPE")
    DATABASE_PORT: ClassVar[int] = os.getenv("DATABASE_PORT")
    POSTGRES_PASSWORD: ClassVar[str] = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_USER: ClassVar[str] = os.getenv("POSTGRES_USER")
    POSTGRES_DB: ClassVar[str] = os.getenv("POSTGRES_DB")
    POSTGRES_HOST: ClassVar[str] = os.getenv("POSTGRES_HOST")
    POSTGRES_HOSTNAME: ClassVar[str] = os.getenv("POSTGRES_HOSTNAME")
    PGADMIN_DEFAULT_EMAIL: ClassVar[str] = os.getenv("PGADMIN_DEFAULT_EMAIL")
    PGADMIN_DEFAULT_PASSWORD: ClassVar[str] = os.getenv(
        "PGADMIN_DEFAULT_PASSWORD"
    )


settings = Settings()
