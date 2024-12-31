from fastapi import APIRouter

import services.user
from models.user import NewUser, User

user_router = APIRouter()

