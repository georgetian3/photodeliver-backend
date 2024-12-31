from uuid import UUID
from sqlalchemy import and_, delete, select
from models.database import get_session
from models.photo import Album, NewAlbum
from services.utils import CrudResult



async def create_album(new_album: NewAlbum) -> Album:
    album = Album(**new_album.model_dump())
    ...
    return album

async def get_album_by_id(album_id: UUID) -> Album | None:
    async with get_session() as session:
        return await session.get(Album, album_id)

async def update_album(album: Album) -> None:
    ...

async def delete_album(album_id: UUID, user_id: UUID) -> CrudResult:
    async with get_session() as session:
        album = await session.get(Album, album_id)
        if not album:
            return CrudResult.DOES_NOT_EXIST
        if album.owner != user_id:
            return CrudResult.NOT_AUTHORITZED
        await session.delete()
        await session.commit()
    return CrudResult.OK