

from uuid import UUID
from models.database import get_session
from models.user import NewUser, User
from services.utils import CrudResult

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

# async def create_user(new_user: NewUser) -> User:
#     user = User(
#         **new_user.model_dump(),
#         id=str(uuid.uuid4()),
#     )
#     async with get_session() as session:
#         session.add(user)
#         await session.commit()
#     return user


# async def get_all_users() -> list[User]:
#     async with get_session() as session:
#         return list(
#             (
#                 await session.execute(select(User).options(joinedload(User.tasks)))
#             ).scalars()
#         )
