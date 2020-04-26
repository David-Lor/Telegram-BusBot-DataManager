"""SETTINGS HANDLER
Declaration of the Settings class and instance that can be used to get any setting required,
using dotenv-settings-handler and python-dotenv.
"""

# # Native # #
from typing import Optional

# # Installed # #
from pydantic import BaseSettings

__all__ = ("settings",)


class Settings(BaseSettings):
    host = "0.0.0.0"
    port = 5000
    name = "Bus Bot Data Manager"
    log_level = "info"
    description: Optional[str]
    mongo_uri = "mongodb://127.0.0.1:27017"
    mongo_stops_db = "busbot_user_data"
    mongo_stops_collection = "stops"

    class Config:
        env_file = ".env"
        env_prefix = "API_"


settings = Settings()
