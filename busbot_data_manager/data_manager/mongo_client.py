"""MONGO
MongoDB database manager
"""

# # Installed # #
from motor import motor_asyncio
from pymongo.collection import Collection

# # Project # #
from busbot_data_manager.settings_handler import settings


def get_collection(loop) -> Collection:
    """Get the MongoDB Stops collection, using the given asyncio Loop"""
    client = motor_asyncio.AsyncIOMotorClient(settings.mongo_uri, io_loop=loop)
    return client[settings.mongo_stops_db][settings.mongo_stops_collection]
