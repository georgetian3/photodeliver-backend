
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from models.display_config import BaseDisplayConfig
from models.user import UserID
from models.utils import UuidId

AlbumID = UUID

class BaseAlbum(SQLModel, table=False):
    name: str = Field(default_factory=lambda: f"New Album {datetime.now().strftime("%y-%m-%d")}")

class NewAlbum(BaseAlbum):
    display_options: BaseDisplayConfig | None

class Album(BaseAlbum, UuidId):
    time_created: datetime = Field(default_factory=lambda: datetime.now(UTC))
    time_updated: datetime = Field(default_factory=lambda: datetime.now(UTC))
    owner: UserID = Field(foreign_key='user.id') # The user who created this album
    preview: int | None = Field(foreign_key='displayconfig.id')

class AlbumSection(SQLModel, UuidId):
    album_id: AlbumID = Field(foreign_key='album.id')
    index: int = Field(nullable=False) # index of this section within an album
    name: str = Field(default='New Section')
    preview: int | None = Field(foreign_key='displayconfig.id')


class BasePhoto(SQLModel):
    ...

class Photo(BasePhoto, UuidId):

    time_created: datetime = Field(default_factory=lambda: datetime.now(UTC))

    section_id: str = Field(foreign_key='section.id') # the album to which this photo belongs
    index: int = Field(nullable=False) # index of this photo within a section

    original_width: int = Field(nullable=False)
    original_height: int = Field(nullable=False)

    preview: int | None = Field(foreign_key='displayconfig.id')

    @property
    def path(self) -> Path:
        return Path()
