from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

import services.album
from apis.utils import create_docs
from services.utils import CrudResult

album_router = APIRouter()


@album_router.get("/albums/{album_id}")
async def get_album(album_id: UUID): ...


@album_router.put("/albums")
async def create_album(): ...


@album_router.post("/albums/{album_id}")
async def update_album(album_id: UUID): ...


DELETE_ALBUM_404 = HTTPException(status.HTTP_404_NOT_FOUND, "Album not found")
DELETE_ALBUM_403 = HTTPException(
    status.HTTP_403_FORBIDDEN, "Cannot delete album, user not owner"
)


@album_router.delete(
    "/albums/{album_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Album deleted successfully",
    responses=create_docs(DELETE_ALBUM_403, DELETE_ALBUM_404),
)
async def delete_album(album_id: UUID):
    result = await services.album.delete_album(album_id, uuid4())
    if result == CrudResult.NOT_AUTHORITZED:
        raise DELETE_ALBUM_403
    if result == CrudResult.DOES_NOT_EXIST:
        raise DELETE_ALBUM_404
