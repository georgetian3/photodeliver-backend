from enum import IntEnum

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class PhotoVisbility(IntEnum):
    HIDDEN = 0 # the photo is hidden from everyone but the owner
    PREVIEW = 1 # anyone with the album ID can see the photo previews
    ORIGINAL = 2 # anyone with the album ID can see the original photos

class DisplayConfig(BaseDisplayConfig, table=True):
    id: int | None = Field(primary_key=True)
