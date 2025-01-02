from uuid import UUID
from sqlalchemy import select
from models.database import get_session
from models.photo import Album, NewAlbum, Photo, PhotoVersion
from services.utils import CrudResult


async def create_album(new_album: NewAlbum, user_id: UUID) -> Album:
    album = Album(**new_album.model_dump(), owner=user_id)
    async with get_session() as session:
        session.add(album)
        await session.commit()
    return album

async def get_user_albums(user_id: UUID) -> list[Album]:
    async with get_session() as session:
        return (await session.execute(select(Album).where(Album.owner==user_id))).scalars()

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
        paths = await session.execute(
            select(PhotoVersion).join(Photo)
        )
        await session.delete(album)
        await session.commit()
    return CrudResult.OK

async def delete_section(section_id: UUID, user_id: UUID):
    ...