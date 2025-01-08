from datetime import UTC, datetime
from enum import IntEnum
from pathlib import Path
from uuid import UUID

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from models.display_config import PhotoVisbility
from models.utils import UuidId


class BaseAlbum(SQLModel):
    name: str = Field(
        default_factory=lambda: f"New Album {datetime.now().strftime("%y-%m-%d")}"
    )


class NewAlbum(BaseAlbum): ...


class Album(BaseAlbum, UuidId, table=True):
    time_created: datetime = Field(default_factory=lambda: datetime.now(UTC))
    time_updated: datetime = Field(default_factory=lambda: datetime.now(UTC))
    owner: UUID = Field(
        foreign_key="user.id", ondelete="CASCADE"
    )  # The user who created this album


class AlbumSection(UuidId, table=True):
    album_id: UUID = Field(foreign_key="album.id", ondelete="CASCADE")
    index: int = Field(nullable=False)  # index of this section within an album
    name: str = Field(default="New Section")


class BasePhoto(SQLModel):
    album_id: UUID = Field(
        foreign_key="album.id", ondelete="CASCADE"
    )  # the album to which this photo belongs
    section_id: UUID | None = Field(
        foreign_key="albumsection.id", ondelete="CASCADE"
    )  # the section to which this photo belongs, can be null
    filename: str = Field(nullable=False)


class NewPhoto(BasePhoto): ...


class Photo(BasePhoto, UuidId, table=True):
    time_uploaded: datetime = Field(default_factory=lambda: datetime.now(UTC))
    index: int = Field(nullable=False)  # index of this photo within a section
    visibility: int = Field(default=PhotoVisbility.HIDDEN)


class SampleConfig(SQLModel):
    quality: int | None = Field(default=None)
    blur: float = Field(default=0.0, le=1.0, ge=0.0)
    scale: float = Field(default=1.0, le=1.0, gt=0.0)
    watermark_text: str | None = Field(default=None)
    watermark_font_size: int = Field(default=200)
    watermark_angle: int = Field(default=45)
    watermark_color: int = Field(default=0xFFFFFF)
    watermark_opacity: float = Field(default=1.0, ge=0.0, le=1.0)
    watermark_x: int | None = Field(default=None)
    watermark_y: int | None = Field(default=None)
    watermark_repeat: bool = Field(default=True)


class BasePhotoVersion(SQLModel):
    quality: int | None = Field(default=None)
    blur: float = Field(default=0, ge=0, le=1)
    preview_scale: float = Field(default=1.0)
    photo_id: UUID = Field(foreign_key="photo.id", ondelete="CASCADE")


class NewPhotoVersion(BasePhotoVersion): ...


class VersionType(IntEnum):
    ORIGINAL = 0
    SAMPLE = 1
    RESIZE = 2


class PhotoVersion(BasePhotoVersion, UuidId, SampleConfig, table=True):
    type: int = Field()  # VersionType
    width: int = Field(nullable=False)
    height: int = Field(nullable=False)
    extra_info: dict | None = Field(
        default=None, sa_column=Column(JSON)
    )  # extra information regarding this album, e.g. styling hints for displaying in frontend

    @property
    def path(self):
        return Path(str(self.id))
