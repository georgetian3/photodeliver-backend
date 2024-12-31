from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

UserID = UUID

class BaseUser(SQLModel, table=False):
    ...

class User(BaseUser, table=True):
    id: UserID | None = Field(primary_key=True, default_factory=uuid4)
    password_hash: str = Field(nullable=False, exclude=True)
    email: str = Field(unique=True)
    is_admin: bool = Field(default=False)

class NewUser(SQLModel, table=False):
    password: str = Field(nullable=False)