from datetime import UTC, datetime
from enum import IntEnum
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel


UserID = int
AlbumID = str


class ErrorResponse(BaseModel):
    detail: str

class BaseUser(SQLModel, table=False):
    ...

class User(BaseUser, table=True):
    id: UserID | None = Field(primary_key=True)
    password_hash: str = Field(nullable=False, exclude=True)
    email: str = Field(unique=True)
    is_admin: bool = Field(default=False)

class NewUser(SQLModel, table=False):
    password: str = Field(nullable=False)

class PhotoVisbility(IntEnum):
    HIDDEN = 0 # the photo is hidden from everyone but the owner
    PREVIEW = 1 # anyone with the album ID can see the photo previews
    ORIGINAL = 2 # anyone with the album ID can see the original photos

class Album(SQLModel):
    id: AlbumID = Field(primary_key=True) # UUID, used as a secret to access album
    time_created: datetime = Field(default_factory=lambda: datetime.now(UTC))
    time_updated: datetime = Field(default_factory=lambda: datetime.now(UTC))
    owner: UserID = Field(foreign_key='user.id') # The user who created this album
    visible: bool = Field(default=True) # Whether the album is visible to anyone with the album ID, visibility of individual photos is controlled by `Photo.permission`
    name: str = Field(default_factory=lambda: f"New Album {datetime.now().strftime("%y-%m-%d")}")
    extra_info: JSON | None = Field(nullable=True) # extra information regarding this album, e.g. styling hints for displaying in frontend


# TODO: should each photo be stored as a file on disk or as binary in DB? Check photoprism implementation

class Photo(SQLModel):
    id: str | None = Field(primary_key=True)

    time_created: datetime = Field(default_factory=lambda: datetime.now(UTC))

    visibility: int = Field(default=PhotoVisbility.HIDDEN)

    album: str = Field(foreign_key='album.id') # the album to which this photo belongs
    album_index: int = Field(nullable=False) # index of this photo within the album
    extra_info: JSON | None = Field(nullable=True) # extra information regarding this photo, e.g. styling hints for displaying in frontend

    hash_original: str = Field(primary_key=True) # the hash of the original photo
    hash_preview: str | None = Field(nullable=True, default=None) # the hash of the preview of the photo, only exists if a preview has been created

    original_width: int = Field(nullable=False)
    original_height: int = Field(nullable=False)

    preview_width: int | None = Field(nullable=True, default=None)
    preview_height: int | None = Field(nullable=True, default=None)

    watermark_text: str | None = Field(nullable=True, default=None)
