from fastapi import FastAPI
from fastapi.routing import APIRoute
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.clients.facebook import FacebookOAuth2
from httpx_oauth.clients.github import GitHubOAuth2

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


if None not in (config.OAUTH_GOOGLE_CLIENT_ID, config.OAUTH_GOOGLE_CLIENT_SECRET):
    api.include_router(
        fastapi_users.get_oauth_router(
            GoogleOAuth2(
                config.OAUTH_GOOGLE_CLIENT_ID, config.OAUTH_GOOGLE_CLIENT_SECRET
            ),
            auth_backend,
            config.STATE_SECRET,
        ),
        prefix="/auth/google",
        tags=["auth"],
    )

if None not in (config.OAUTH_FACEBOOK_CLIENT_ID, config.OAUTH_FACEBOOK_CLIENT_SECRET):
    api.include_router(
        fastapi_users.get_oauth_router(
            FacebookOAuth2(
                config.OAUTH_FACEBOOK_CLIENT_ID, config.OAUTH_FACEBOOK_CLIENT_SECRET,
                ["https://www.googleapis.com/auth/userinfo.email"]
            ),
            auth_backend,
            config.STATE_SECRET,
        ),
        prefix="/auth/facebook",
        tags=["auth"],
    )

if None not in (config.OAUTH_GITHUB_CLIENT_ID, config.OAUTH_GITHUB_CLIENT_SECRET):
    api.include_router(
        fastapi_users.get_oauth_router(
            GitHubOAuth2(
                config.OAUTH_GITHUB_CLIENT_ID, config.OAUTH_GITHUB_CLIENT_SECRET, ["user:email"]
            ),
            auth_backend,
            config.STATE_SECRET
        ),
        prefix="/auth/github",
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
