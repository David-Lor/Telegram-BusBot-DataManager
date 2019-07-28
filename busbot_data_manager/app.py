"""APP
Module with all the available endpoints and the FastAPI initialization.
"""

# # Installed # #
import uvicorn
import fastapi

# # Project # #
from .settings_handler import settings
from . import data_manager

# # Package # #
from .entities import *
from .app_exceptions import *
from .app_responses import *

__all__ = ("app", "run")

app = fastapi.FastAPI(
    title=settings.name,
    description=settings.description,
    version=settings.version
)


@app.get("/status")
async def endpoint_get_status():
    """Get API Status
    """
    return OKResponse


@app.get("/stops/{userid}")
async def endpoint_get_stops(userid: int):
    """Get all the saved stops for the given User.
    """
    with manage_endpoint_exceptions():
        stops = await data_manager.get_user_stops(userid)
        return [s.get_api_dict() for s in stops]


@app.post("/stops")
async def endpoint_insert_stop(stop: SavedStop):
    """Insert or update a Stop to a User.
    To remove the name from a Stop, set it to false.
    """
    with manage_endpoint_exceptions():
        await data_manager.save_stop(stop)
        return CreatedResponse


@app.delete("/stops/{userid}/{stopid}")
async def endpoint_delete_stop(userid: int, stopid: int):
    """Delete the given Stop from the given User.
    """
    with manage_endpoint_exceptions():
        await data_manager.delete_stop(userid, stopid)
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


if __name__ == '__main__':
    run()