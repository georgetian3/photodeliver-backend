from fastapi import APIRouter

photo_router = APIRouter()


@photo_router.get("/photos")
async def get_photos(): ...


@photo_router.put("/photos")
async def upload_photos(): ...


@photo_router.post("/photos")
async def update_photos(): ...


@photo_router.delete("/photos")
async def delete_photos(): ...
