

from models.database import get_session
from models.user import NewUser, User



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
