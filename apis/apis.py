from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from apis.users import user_router
from apis.albums import album_router

api = FastAPI()

api.include_router(album_router)
api.include_router(user_router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
