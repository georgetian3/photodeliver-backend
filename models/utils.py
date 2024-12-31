from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class UuidId(SQLModel, table=False):
    id: UUID = Field(primary_key=True, default_factory=uuid4)