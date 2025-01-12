import asyncio
import pytest
from fastapi import UploadFile

from services.album import create_album
from services.media import upload_media
from models.media import Album, MediaType, NewAlbum, NewMedia
from models.user import User
from services.user import create_user, get_user_by_email


@pytest.fixture
async def user_fixture() -> User:
    email = "test@example.com"
    try:
        return await create_user(email, "password")
    except:
        return await get_user_by_email(email)
    
@pytest.fixture
async def album_fixture(user_fixture: User) -> Album:
    return await create_album(NewAlbum(), user_fixture)

async def test_upload_media(user_fixture: User, album_fixture: Album):
    upload_file = UploadFile(file=open('test.jpg', 'rb'), filename='test.jpg')
    await upload_media(
        [upload_file],
        [NewMedia(album_id=album_fixture.id, media_type=MediaType.VIDEO, filename='test.jpg')],
        user=user_fixture,
    )