from fastapi import FastAPI
from apis.users import user_router
from apis.albums import album_router
from apis.sections import section_router
from apis.photos import photo_router
from apis.users import user_router

api = FastAPI()

api.include_router(album_router)
api.include_router(section_router)
api.include_router(photo_router)
api.include_router(user_router)
