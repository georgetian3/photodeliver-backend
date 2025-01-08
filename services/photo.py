from io import BytesIO
from pathlib import Path
from uuid import UUID

import aiofiles
from fastapi import UploadFile

import config
from models.database import get_session
from models.photo import NewPhoto, NewPhotoVersion, Photo, PhotoVersion, VersionType

from PIL.ImageFile import ImageFile

from models.user import User
from services.logging import get_logger
from watermarkipy import blur, watermark

logger = get_logger(__name__)


async def create_sample_photo(
    image: ImageFile, photo_version: PhotoVersion
) -> ImageFile:
    # image = await resize_image(image, photo_version)
    # image = await blur_image(image, photo_version)
    # image = watermark(image, photo_version)
    return image


async def get_photo_dimensions() -> tuple[int, int]:
    return 0, 0


async def create_photo_version(
    original: BytesIO, new_photo_version: NewPhotoVersion
) -> PhotoVersion:
    photo_version = PhotoVersion(
        **new_photo_version.model_dump(),
    )
    return photo_version


async def upload_photos(photos: list[UploadFile], album_id: UUID, user: User) -> None:

    async with get_session() as session:
        for photo in photos:
            new_photo = Photo(album_id=album_id)
            photo_version = PhotoVersion(type=VersionType.ORIGINAL.value)
            async with aiofiles.open(photo_version.path, "wb") as f:
                while chunk := await photo.read(config.CHUNK_SIZE):
                    await f.write(chunk)
            session.add(new_photo)
            session.add(photo_version)
        await session.commit()

    return
    photo = Photo()
    width, height = await get_photo_dimensions()
    photo_version = await create_photo_version(BytesIO, NewPhotoVersion())
    async with get_session() as session:
        session.add(photo)
        session.add(photo_version)
        await session.commit()


async def strip_exif_metadata() -> None: ...


async def create_originals() -> None:
    await strip_exif_metadata()
    ...


async def get_previews() -> list[PhotoVersion]:
    return []


async def get_originals() -> list[PhotoVersion]:
    return []
