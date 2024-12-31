from models.database import get_session
from models.exceptions import UserNotAlbumOwnerError
from models.models import Album, AlbumID, UserID

async def modify_album_visibility(user_id: UserID, album_id: AlbumID, new_visibility: bool) -> None:
    """
    :param user_id: ID of user modifying the album
    :param album_id: ID of album being modified
    :param new_visibility: the new visibility of the album
    :returns: `None`
    :raises: `UserNotAlbumOwnerError` if the user is not the owner of the album
    """
    async with get_session() as session:
        album = await session.get(Album, album_id)
        if album.owner != user_id:
            raise UserNotAlbumOwnerError()
        album.visible = new_visibility
        await session.commit()