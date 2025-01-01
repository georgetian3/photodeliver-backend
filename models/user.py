from sqlmodel import Field, SQLModel

from models.utils import UuidId

class BaseUser(SQLModel, table=False):
    email: str = Field(unique=True)

class NewUser(BaseUser, table=False):
    password: str = Field(nullable=False)

class User(BaseUser, UuidId, table=True):
    password_hash: str = Field(nullable=False, exclude=True)
    is_admin: bool = Field(default=False)
    active: bool = Field(default=True)