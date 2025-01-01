
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from models.display_config import PhotoVisbility
from models.utils import UuidId

class BaseAlbum(SQLModel, table=False):
    name: str = Field(default_factory=lambda: f"New Album {datetime.now().strftime("%y-%m-%d")}")

class NewAlbum(BaseAlbum):
    ...

class Album(BaseAlbum, UuidId, table=True):
    time_created: datetime = Field(default_factory=lambda: datetime.now(UTC))
    time_updated: datetime = Field(default_factory=lambda: datetime.now(UTC))
    owner: UUID = Field(foreign_key="user.id", ondelete="CASCADE") # The user who created this album

class AlbumSection(UuidId, table=True):
    album_id: UUID = Field(foreign_key='album.id', ondelete="CASCADE")
    index: int = Field(nullable=False) # index of this section within an album
    name: str = Field(default='New Section')


class BasePhoto(SQLModel):
    album_id: UUID = Field(foreign_key="album.id", ondelete="CASCADE")
    section_id: UUID | None = Field(foreign_key="albumsection.id", ondelete="CASCADE") # the album to which this photo belongs

class NewPhoto(SQLModel, table=False):
    ...

class Photo(BasePhoto, UuidId, table=True):
    time_uploaded: datetime = Field(default_factory=lambda: datetime.now(UTC))
    index: int = Field(nullable=False) # index of this photo within a section
    visibility: int = Field(default=PhotoVisbility.HIDDEN)
    original_filename: str = Field(nullable=False)


class PhotoVersion(UuidId, table=True):
    photo_id: UUID = Field(foreign_key='photo.id', ondelete="CASCADE")
    original: bool = Field(nullable=False)
    width: int = Field(nullable=False)
    height: int = Field(nullable=False)
    quality: int | None = Field(default=None)
    blur: bool = Field(default=False)
    watermark_text: str | None = Field(default=None)
    preview_scale: float = Field(default=1.0)
    extra_info: dict | None = Field(default=None, sa_column=Column(JSON)) # extra information regarding this album, e.g. styling hints for displaying in frontend
    @property
    def path(self):
        return Path(self.id)