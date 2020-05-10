"""WRITER
Write data (insert, modify or delete) on MongoDB
"""

# # Native # #
import asyncio

# # Installed # #
from pymongo.results import *

# # Project # #
from busbot_data_manager.data_manager.mongo_client import get_collection
from busbot_data_manager.data_manager.reader import is_stop_saved
from busbot_data_manager.entities import *

__all__ = ("save_stop", "modify_stop", "delete_stop", "delete_all_stops")


async def save_stop(stop: SavedStop):
    """Insert a new Stop or modify if already exists.
    :raise: AssertionError
    """
    loop = asyncio.get_event_loop()
    if not await is_stop_saved(stop.user_id, stop.stop_id):
        result: InsertOneResult = await get_collection(loop).insert_one(stop.get_mongo_dict())
        assert result.acknowledged
    else:
        await modify_stop(stop)


async def modify_stop(stop: SavedStop):
    """Modify a Stop previously saved with a new one.
    :raise: AssertionError
    """
    loop = asyncio.get_event_loop()
    result: UpdateResult = await get_collection(loop).update_one(
        stop.get_mongo_filter(), stop.get_mongo_update_dict()
    )
    assert result.matched_count == 1


async def delete_stop(user_id: UserId, stop_id: StopId):
    """Delete a saved stop given the User ID and the Stop ID.
    :raise: FileNotFoundError
    """
    loop = asyncio.get_event_loop()
    result: DeleteResult = await get_collection(loop).delete_one({"user_id": user_id, "stop_id": stop_id})
    if result.deleted_count == 0:
        raise FileNotFoundError()


async def delete_all_stops(user_id: UserId):
    """Delete all the saved stops of the given User.
    """
    loop = asyncio.get_event_loop()
    await get_collection(loop).delete_many({"user_id": user_id})
