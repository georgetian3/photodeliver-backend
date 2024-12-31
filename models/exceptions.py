from pydantic import BaseModel


class UserNotAlbumOwnerError(Exception): ...



class ErrorResponse(BaseModel):
    detail: str

