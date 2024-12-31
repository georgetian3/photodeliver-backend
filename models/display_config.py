from enum import IntEnum

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class PhotoVisbility(IntEnum):
    HIDDEN = 0 # the photo is hidden from everyone but the owner
    PREVIEW = 1 # anyone with the album ID can see the photo previews
    ORIGINAL = 2 # anyone with the album ID can see the original photos

class BaseDisplayConfig(SQLModel, table=False):
    visibility: int = Field(default=PhotoVisbility.HIDDEN)
    blur: bool = Field(default=False)
    watermark_text: str | None = Field(default=None)
    preview_width: int | None = Field(default=None)
    preview_height: int | None = Field(default=None)
    extra_info: dict | None = Field(default=None, sa_column=Column(JSON)) # extra information regarding this album, e.g. styling hints for displaying in frontend

class DisplayConfig(BaseDisplayConfig):
    id: int | None = Field(primary_key=True)
