import os

import toml
from dotenv import load_dotenv
from aioredis import Redis

load_dotenv()


class Config:
    # Database configurations
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_PORT = os.getenv("DB_PORT")

    # Celery configurations
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

    # Auth Secret
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Redis configurations
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_DB = os.getenv("REDIS_DB")
    REDIS_URL_STR = os.getenv("REDIS_URL")
    REDIS_URL = Redis.from_url(REDIS_URL_STR)

    @staticmethod
    def get_database_url():
        return f"postgresql+asyncpg://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"

    @staticmethod
    def load_toml_config():
        """
        Load the configuration from the pyproject.toml file.

        Returns:
            dict: The loaded configuration as a dictionary.
        """
        with open("pyproject.toml", "r") as toml_file:
            return toml.load(toml_file)
