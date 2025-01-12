from io import BytesIO

from fastapi import UploadFile
from PIL.ImageFile import ImageFile

from models.media import Media, MediaVersion, NewMedia, NewMediaVersion
from models.user import User
from services.logging import get_logger
from services.storage_backend import STORAGE_BACKEND
from services.tasks import process_new_media

logger = get_logger(__name__)


async def create_sample_media(
    image: ImageFile, media_version: MediaVersion
) -> ImageFile:
    # image = await resize_image(image, media_version)
    # image = await blur_image(image, media_version)
    # image = watermark(image, media_version)
    return image


async def get_media_dimensions() -> tuple[int, int]:
    return 0, 0


async def create_media_version(
    original: BytesIO, new_media_version: NewMediaVersion
) -> MediaVersion:
    media_version = MediaVersion(
        **new_media_version.model_dump(),
    )
    return media_version


class MediaFileMetadataMismatch(Exception): ...




async def upload_media(media_files: list[UploadFile], new_media: list[NewMedia], user: User) -> None:
    # TODO: Check user storage limits etc?

    # check 1-1 relationship
    if (
        len(media_files) != len(new_media) # number of new media
        or len(file_set := {file.filename for file in media_files}) != len(media_files) # dups in files
        or len(media_set := {media.filename for media in new_media}) != len(new_media) # dups in medias
        or file_set != media_set # file-media equality
    ):
        raise MediaFileMetadataMismatch()
    

    # TODO: insert `NewMedia`s into db whilst checking for album + section ownership
    media_map = {
        new_media.filename: Media(**new_media.model_dump(), processing=True) for new_media in new_media
    }
    # update index


    # create `media_version` ids without saving to DB, will do so in celery job
    media_versions = [MediaVersion() for _ in media_files]
    # write files based on ids
    await STORAGE_BACKEND.write(media_files, [media_version.path for media_version in media_versions])

    for media_version in media_versions:
        process_new_media.delay(media_version)
    # TODO: enqueue jobs based on `media_version` ids
    
    return

async def strip_exif_metadata() -> None: ...


async def create_originals() -> None:
    await strip_exif_metadata()
    ...


async def get_previews() -> list[MediaVersion]:
    return []


async def get_originals() -> list[MediaVersion]:
    return []
