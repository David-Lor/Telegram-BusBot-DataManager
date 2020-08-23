"""APP EXCEPTIONS
Exception manager (as contextmanager) to convert internal exceptions to HTTP exceptions, properly described.
Custom exceptions raised by internal functions.
"""

# # Native # #
import contextlib

# # Installed # #
import fastapi
from fastapi import status as statuscode

__all__ = ("manage_endpoint_exceptions",)


@contextlib.contextmanager
def manage_endpoint_exceptions():
    """ContextManager to catch internal exceptions and return a related HTTP Status Code and Error to the client.
    """
    try:
        yield
    except (StopIteration, FileNotFoundError):
        raise fastapi.HTTPException(
            status_code=statuscode.HTTP_404_NOT_FOUND,
            detail="Stop not found for this user"
        )
    except AssertionError:
        raise fastapi.HTTPException(
            status_code=statuscode.HTTP_409_CONFLICT,
            detail="Internal conflict detected. The admin must review the logs."
        )
