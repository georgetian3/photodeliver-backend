from sqlalchemy import and_, delete, select
from models.database import get_session
from models.exceptions import UserNotAlbumOwnerError
from models.photo import Album, AlbumID, NewAlbum
from models.user import UserID
from services.utils import CrudResult



async def create_album(new_album: NewAlbum) -> Album:
    album = Album(**new_album.model_dump())
    ...
    return album

async def get_album_by_id(album_id: AlbumID) -> Album | None:
    async with get_session() as session:
        return await session.get(Album, album_id)

async def update_album(album: Album) -> None:
    ...

async def delete_album(user_id: UserID, album_id: AlbumID) -> CrudResult:
    async with get_session() as session:
        album = await session.get(Album, album_id)
        if not album:
            return CrudResult.DOES_NOT_EXIST
        if album.owner != user_id:
            return CrudResult.NOT_AUTHORITZED
        await session.delete()
        await session.commit()
        return CrudResult.OK