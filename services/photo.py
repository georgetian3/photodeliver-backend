


from models.photo import NewPhoto, Photo, PhotoVersion


async def watermark_photo() -> None:
    ...

async def compress_photo(photo: Photo) -> None:
    ...


async def create_preview() -> None:
    compress_photo()
    watermark_photo()


async def create_previews() -> None:
    ...

async def get_photo_dimensions() -> tuple[int, int]:
    return 0, 0


async def upload_photo(new_photo: NewPhoto) -> None:
    photo = Photo()
    width, height = get_photo_dimensions
    photo_version = PhotoVersion(
        original=True,
        width=width,
        height=height,
    )

async def strip_exif_metadata() -> None:
    ...

async def create_originals() -> None:
    strip_exif_metadata()
    ...

async def get_previews() -> list:
    ...

async def get_originals() -> list:
    ...

