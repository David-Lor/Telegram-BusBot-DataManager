"""WRITER
Write data (insert, modify or delete) on MongoDB
"""

# # Native # #
import asyncio

# # Installed # #
from pymongo.results import *

# # Project # #
from ..entities import *

# # Package # #
from .mongo_client import get_collection
from .reader import is_stop_saved

__all__ = ("save_stop", "modify_stop", "delete_stop")


async def save_stop(stop: SavedStop):
    """Insert a new Stop or modify if already exists.
    :raise: AssertionError
    """
    loop = asyncio.get_event_loop()
    if not await is_stop_saved(stop.userid, stop.stopid):
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


async def delete_stop(userid: int, stopid: int):
    """Delete a saved stop given the User ID and the Stop ID.
    :raise: FileNotFoundError
    """
    loop = asyncio.get_event_loop()
    result: DeleteResult = await get_collection(loop).delete_one({"userid": userid, "stopid": stopid})
    if result.deleted_count == 0:
        raise FileNotFoundError()
