from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute
from apis.users import user_router
from apis.albums import album_router
from apis.sections import section_router
from apis.photos import photo_router
from apis.users import user_router
from services.user import fastapi_users, auth_backend, current_active_user
from models.user import User, UserRead, UserCreate, UserUpdate



api = FastAPI()

api.include_router(album_router, tags=["album"])
api.include_router(section_router, tags=["section"])
api.include_router(photo_router, tags=["photo"])
api.include_router(user_router, tags=["user"])


api.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
api.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@api.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}



"""
Simplify operation IDs so that generated API clients have simpler function
names.

Should be called only after all routes have been added.

# https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#using-the-path-operation-function-name-as-the-operationid
"""
for route in api.routes:
    if isinstance(route, APIRoute):
        route.operation_id = route.name