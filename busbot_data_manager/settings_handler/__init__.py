"""SETTINGS HANDLER
Declaration of the Settings class and instance that can be used to get any setting required,
using dotenv-settings-handler and python-dotenv.
"""

# # Native # #
from typing import Optional

# # Installed # #
# noinspection PyPackageRequirements
from dotenv import load_dotenv
from dotenv_settings_handler import BaseSettingsHandler

__all__ = ("settings",)

load_dotenv()


class Settings(BaseSettingsHandler):
    host = "0.0.0.0"
    port = 5000
    name = "Bus Bot Data Manager"
    version = "0.0.1"
    log_level = "info"
    description: Optional[str]
    mongo_uri = "mongodb://127.0.0.1:27017"
    mongo_stops_db = "busbot_user_data"
    mongo_stops_collection = "stops"

    class Config:
        case_insensitive = True
        env_prefix = "API_"


settings = Settings()
