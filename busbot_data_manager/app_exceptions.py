"""APP EXCEPTIONS
Exception manager (as contextmanager) to convert internal exceptions to HTTP exceptions, properly described
"""

# # Native # #
import contextlib

# # Installed # #
import fastapi
# noinspection PyPackageRequirements
from starlette import status as statuscode

__all__ = ("manage_endpoint_exceptions",)


@contextlib.contextmanager
def manage_endpoint_exceptions():
    """ContextManager to catch internal exceptions and return an HTTP Status Code to the client,
    depending on the exception raised.
    """
    try:
        yield
    except StopIteration:
        raise fastapi.HTTPException(
            status_code=statuscode.HTTP_404_NOT_FOUND, detail="Stop not saved for this user"
        )
