


async def watermark_photo() -> None:
    ...

async def compress_photo() -> None:
    ...


async def create_preview() -> None:
    compress_photo()
    watermark_photo()


async def create_previews() -> None:
    ...



async def strip_exif_metadata() -> None:
    ...

async def create_originals() -> None:
    strip_exif_metadata()
    ...

async def get_previews() -> list:
    ...

async def get_originals() -> list:
    ...

