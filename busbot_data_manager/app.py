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
    return "OK"
    # TODO Return as plain text


@app.get("/stops/{userid}")
async def endpoint_get_stops(userid: int):
    """Get all the saved stops for the given User.
    """
    with manage_endpoint_exceptions():
        return [s.get_api_dict() for s in data_manager.get_user_stops(userid)]


@app.post("/stops")
async def endpoint_insert_stop(stop: SavedStop):
    with manage_endpoint_exceptions():
        # TODO properly return
        return data_manager.save_stop(stop)


@app.delete("/stops/{userid}/{stopid}")
async def endpoint_delete_stop(userid: int, stopid: int):
    """Delete the given Stop from the given User.
    """
    with manage_endpoint_exceptions():
        # TODO properly return
        return data_manager.delete_stop(userid, stopid)


@app.patch("/stops/{userid}/{stopid}")
async def endpoint_modify_stop(userid: int, stopid: int, stop: SavedStop):
    with manage_endpoint_exceptions():
        # TODO properly return
        return data_manager.modify_stop(userid, stopid, stop)


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
