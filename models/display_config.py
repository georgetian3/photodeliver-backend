from enum import IntEnum


class MediaVisibility(IntEnum):
    HIDDEN = 0  # the media is hidden from everyone but the owner
    PREVIEW = 1  # anyone with the album ID can see the media previews
    ORIGINAL = 2  # anyone with the album ID can see the original media
