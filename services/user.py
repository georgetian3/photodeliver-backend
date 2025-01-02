

from uuid import UUID

from sqlalchemy import select
import config
from models.database import get_session
from models.user import User
from services import logging
from services.utils import CrudResult
from argon2 import hash_password, verify_password

logger = logging.get_logger(__name__)


async def _create_user(user: User) -> None:
    async with get_session() as session:
        session.add(user)
        await session.commit()

# async def create_user(new_user: NewUser, is_admin: bool = False) -> User:
#     user = User(
#         **new_user.model_dump(),
#         password_hash=hash_password(new_user.password.encode("utf-8")).decode("utf-8"),
#         is_admin=is_admin
#     )
#     await _create_user(user)
#     return user


# async def create_admin_from_config() -> None:
#     new_user = NewUser(
#         email=config.ADMIN_EMAIL,
#         password=config.ADMIN_PASSWORD,
#     )
#     try:
#         await create_user(new_user, True)
#     except Exception as e:
#         logger.warning(f"Cannot create admin: {e}")


async def set_user_active(user_id: UUID, active: bool) -> CrudResult:
    """
    Modify a user to be (in)active. Admins cannot be deactivated
    :param user_id: user to be modified
    :param active: new activity status
    :returns: `CrudResult`
    - `DOES_NOT_EXIST`: `user_id` does not exist
    - `NOT_AUTHORIZED`: attempted to update an admin user
    - `OK`: update successful
    """
    async with get_session() as session:
        user = await session.get(User, user_id)
        if not user:
            return CrudResult.DOES_NOT_EXIST
        if user.is_admin:
            return CrudResult.NOT_AUTHORITZED
        user.active = active
        session.add(user)
        await session.commit()
    return CrudResult.OK


async def get_user_by_id(user_id: UUID) -> User | None:
    async with get_session() as session:
        return session.get(User, user_id)
    
async def get_user_by_email(email: str) -> User | None:
    async with get_session() as session:
        return (await session.query(User).filter(User.email==email)).first()

# async def get_all_users() -> list[User]:
#     async with get_session() as session:
#         return list(
#             (
#                 await session.execute(select(User).options(joinedload(User.tasks)))
#             ).scalars()
#         )


import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlmodel import SQLModelUserDatabaseAsync

from models.database import get_user_db
from models.user import User

SECRET = "SECRET"


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Request | None = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLModelUserDatabaseAsync = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy[models.UP, models.ID]:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)