

from fastapi import APIRouter, HTTPException, status
from apis.utils import create_docs
import services.album
from services.utils import CrudResult

album_router = APIRouter()


@album_router.get("/album/{album_id}")
async def get_album(album_id: str):
    ...

@album_router.put("/album")
async def create_album():
    ...

@album_router.post("/album/{album_id}")
async def update_album(album_id: str):
    ...




DELETE_ALBUM_404 = HTTPException(status.HTTP_404_NOT_FOUND, 'Album not found')
DELETE_ALBUM_403 = HTTPException(status.HTTP_403_FORBIDDEN, 'Cannot delete album, user not owner')

@album_router.delete("/album/{album_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=create_docs(DELETE_ALBUM_403, DELETE_ALBUM_404)
)
async def delete_album(album_id: str):
    result = await services.album.delete_album('asdf', album_id)
    if result == CrudResult.DOES_NOT_EXIST:
        raise DELETE_ALBUM_404
    if result == CrudResult.NOT_AUTHORITZED:
        raise DELETE_ALBUM_403