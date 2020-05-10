"""APP
Module with all the available endpoints and the FastAPI initialization.
"""

# # Installed # #
import uvicorn
import fastapi

# # Project # #
from busbot_data_manager import data_manager
from busbot_data_manager.entities import *
from busbot_data_manager.app_exceptions import *
from busbot_data_manager.app_responses import *
from busbot_data_manager.settings_handler import settings

__all__ = ("app", "run")

app = fastapi.FastAPI(
    title=settings.name,
    description=settings.description
)


@app.get("/status")
async def endpoint_get_status():
    """Get API Status
    """
    return OKResponse


@app.get("/stops/{user_id}")
async def endpoint_get_stops(user_id: UserId):
    """Get all the saved stops for the given User.
    """
    with manage_endpoint_exceptions():
        stops = await data_manager.get_user_stops(user_id)
        return [s.get_api_dict() for s in stops]


@app.post("/stops")
async def endpoint_insert_stop(stop: SavedStop):
    """Insert or update a Stop to a User.
    To remove the name from a Stop, set it to null or do not send.
    """
    with manage_endpoint_exceptions():
        await data_manager.save_stop(stop)
        return CreatedResponse


@app.delete("/stops/{user_id}/{stop_id}")
async def endpoint_delete_stop(user_id: UserId, stop_id: StopId):
    """Delete the given Stop from the given User.
    """
    with manage_endpoint_exceptions():
        await data_manager.delete_stop(user_id, stop_id)
        return NoContentResponse


@app.delete("/stops/{user_id}")
async def endpoint_delete_all_stops(user_id: UserId):
    """Delete all saved Stops from the given User.
    """
    with manage_endpoint_exceptions():
        await data_manager.delete_all_stops(user_id)
        return NoContentResponse


def run():
    """Run the API using Uvicorn
    """
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level
    )
