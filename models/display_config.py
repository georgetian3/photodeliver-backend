from enum import IntEnum

class PhotoVisbility(IntEnum):
    HIDDEN = 0 # the photo is hidden from everyone but the owner
    PREVIEW = 1 # anyone with the album ID can see the photo previews
    ORIGINAL = 2 # anyone with the album ID can see the original photos
