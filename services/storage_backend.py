from typing import BinaryIO, Iterable

import aiofiles
from fastapi import UploadFile

import config


class BaseStorageBackend:

    def get_path(file: UploadFile) -> str:
        raise NotImplementedError()
    
    async def read(self) -> None:
        raise NotImplementedError()

    async def write(self, files: Iterable[BinaryIO]) -> None:
        raise NotImplementedError()


class MissingFilenameError(Exception): ...

class LocalFileStorageBackend(BaseStorageBackend):

    async def read(self):
        ...

    async def write(self, files: Iterable[BinaryIO]):
        for file in files:
            async with aiofiles.open(file, "wb") as f:
                while chunk := await file.read(config.CHUNK_SIZE):
                    await f.write(chunk)

if config.STORAGE_BACKEND.lower() == "s3":
    raise NotImplementedError()
else:
    STORAGE_BACKEND = LocalFileStorageBackend()