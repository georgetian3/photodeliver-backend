from fastapi import FastAPI
from fastapi.routing import APIRoute
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.clients.facebook import FacebookOAuth2

from apis.albums import album_router
from apis.photos import photo_router
from apis.sections import section_router
import config
from models.user import UserCreate, UserRead, UserUpdate
from services.user import auth_backend, fastapi_users

api = FastAPI()

api.include_router(album_router, tags=["album"])
api.include_router(section_router, tags=["section"])
api.include_router(photo_router, tags=["photo"])


google_oauth_client = GoogleOAuth2(config.OAUTH_GOOGLE_CLIENT_ID, config.OAUTH_GOOGLE_CLIENT_SECRET)

api.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, "SECRET"),
    prefix="/auth/google",
    tags=["auth"],
)

api.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["auth"]
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

"""
Simplify operation IDs so that generated API clients have simpler function
names.

Should be called only after all routes have been added.

# https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#using-the-path-operation-function-name-as-the-operationid
"""
for route in api.routes:
    if isinstance(route, APIRoute):
        route.operation_id = route.name
