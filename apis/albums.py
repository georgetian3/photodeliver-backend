

from fastapi import APIRouter


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

@album_router.delete("/album/{album_id}")
async def delete_album(album_id: str):
    ...
