from uuid import UUID

from fastapi_users import schemas
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB


class User(SQLModelBaseUserDB, table=True): ...


class UserRead(schemas.BaseUser[UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
