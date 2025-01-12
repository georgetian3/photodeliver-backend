
from fastapi import APIRouter, Depends, UploadFile

import services.media
from apis.utils import create_docs
from models.media import NewMedia
from models.user import User
from services.user import current_active_verified_user

media_router = APIRouter()


@media_router.get("/media")
async def get_media(): ...


@media_router.put(
    "/media",
    description="""
Uploads media to the specified album and section (optional).

There must be a 1-1 correspondance between elements of `media_files` and `new_media`.

""",
    responses=create_docs()

)
async def upload_media(
    media_files: list[UploadFile],
    new_media: list[NewMedia],
    user: User = Depends(current_active_verified_user),
):
    await services.media.upload_media(media_files, new_media, user)


@media_router.post("/media")
async def update_media(): ...


@media_router.delete("/media")
async def delete_media(): ...
