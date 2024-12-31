from enum import Enum


class CrudResult(Enum):
    OK = 0
    DOES_NOT_EXIST = 1
    NOT_AUTHORITZED = 2