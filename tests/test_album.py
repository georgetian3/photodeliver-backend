import pytest

from models.photo import NewAlbum
from services.album import create_album


# @pytest.mark.asyncio
# async def test_create_album():
#     try:
#         user = await create_user(NewUser(email="me@georgetian.com", password="password"))
#     except:
#     await create_album(NewAlbum(name="test album"), user.id)