from uuid import UUID
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from fastapi_users import schemas


class User(SQLModelBaseUserDB, table=True):
    ...


class UserRead(schemas.BaseUser[UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass