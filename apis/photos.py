from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile

from models.user import User
from services.user import current_active_verified_user
import services.photo

photo_router = APIRouter()


@photo_router.get("/photos")
async def get_photos(): ...


@photo_router.put("/photos")
async def upload_photos(photos: list[UploadFile], album_id: UUID, user: User = Depends(current_active_verified_user)):
    await services.photo.upload_photos(photos, album_id, user)

@photo_router.post("/photos")
async def update_photos(): ...


@photo_router.delete("/photos")
async def delete_photos(): ...
