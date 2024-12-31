from typing import Any
from fastapi import HTTPException, status
from pydantic import BaseModel

from models.exceptions import ErrorResponse

NOT_AUTHENTICATED = "Not authenticated"
NOT_ADMIN = "Admin privileges required"
NOT_FOUND = "Object not found"

NOT_AUTHENTICATED_HTTP_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail=NOT_AUTHENTICATED
)
NOT_ADMIN_HTTP_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN
)
NOT_FOUND_HTTP_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND
)
HTTP_400_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail=''
)

def create_doc(exception: HTTPException):
    return {
        exception.status_code: {
            "model": ErrorResponse,
            "description": exception.detail
        }
    }


def create_docs(*args: list[HTTPException]) -> dict[int, dict[str, Any]]:
    docs = {}
    for exception in args:
        docs |= create_doc(exception)
    return docs