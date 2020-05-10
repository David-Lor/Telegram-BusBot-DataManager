"""APP RESPONSES
Common simple responses
"""

# # Installed # #
from fastapi import Response
from fastapi import status as statuscode

__all__ = ("OKResponse", "CreatedResponse", "NoContentResponse")


OKResponse = Response(
    content="OK",
    media_type="text/plain",
    status_code=statuscode.HTTP_200_OK
)

CreatedResponse = Response(
    content="OK",
    media_type="text/plain",
    status_code=statuscode.HTTP_201_CREATED
)

NoContentResponse = Response(
    content="OK",
    media_type="text/plain",
    status_code=statuscode.HTTP_204_NO_CONTENT
)
