"""READER
Read data from MongoDB
"""

# # Native # #
import asyncio

# # Project # #
from ..entities import *

# # Package # #
from .mongo_client import get_collection

__all__ = ("get_user_stops", "is_stop_saved")


async def get_user_stops(userid: int) -> SavedStopList:
    """Get all the Saved Stops for the given User ID.
    If no stops are found, an empty array is returned.
    :return: List of SavedStop objects
    """
    loop = asyncio.get_event_loop()
    cursor = get_collection(loop).find({"userid": userid})
    return [SavedStop(**doc) async for doc in cursor]


async def is_stop_saved(userid: int, stopid: int) -> bool:
    """Check if the given Stop ID is saved by the given User ID.
    :return: True if found
    """
    # TODO Mongo query vs. Python load & query?
    user_stops = await get_user_stops(userid)
    return any(stop for stop in user_stops if stop.userid == userid and stop.stopid == stopid)
