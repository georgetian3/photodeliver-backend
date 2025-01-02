


from io import BytesIO
from models.database import get_session
from models.photo import NewPhoto, NewPhotoVersion, Photo, PhotoVersion


async def watermark_photo(photo: Photo) -> None:
    ...

async def compress_photo(photo: Photo) -> None:
    ...


async def create_preview(photo: Photo) -> None:
    await compress_photo(photo)
    await watermark_photo(photo)


async def create_previews() -> None:
    ...

async def get_photo_dimensions() -> tuple[int, int]:
    return 0, 0


async def create_photo_version(original: BytesIO, new_photo_version: NewPhotoVersion) -> PhotoVersion:
    ...

async def create_photo(new_photo: NewPhoto) -> None:
    photo = Photo()
    width, height = await get_photo_dimensions()
    photo_version = PhotoVersion(
        original=True,
        width=width,
        height=height,
    )
    async with get_session() as session:
        ...

async def strip_exif_metadata() -> None:
    ...

async def create_originals() -> None:
    await strip_exif_metadata()
    ...

async def get_previews() -> list[PhotoVersion]:
    return []

async def get_originals() -> list[PhotoVersion]:
    return []

