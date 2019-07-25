"""APP
Module with all the available endpoints and the FastAPI initialization.
"""

# # Native # #
import asyncio
import contextlib

# # Installed # #
import uvicorn
import fastapi

# # Project # #
from .settings_handler import settings

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


@app.get("/")
async def endpoint_get_root():
    """Root endpoint
    """
    return {
        "status": "Hello World!"
    }


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
