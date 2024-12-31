from sqlmodel import Field, SQLModel

from models.utils import UuidId

class BaseUser(SQLModel, table=False):
    ...

class User(BaseUser, UuidId, table=True):
    password_hash: str = Field(nullable=False, exclude=True)
    email: str = Field(unique=True)
    is_admin: bool = Field(default=False)

class NewUser(SQLModel, table=False):
    password: str = Field(nullable=False)