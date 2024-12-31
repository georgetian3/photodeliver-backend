from fastapi import APIRouter

import services.user
from models.models import NewUser, User

user_router = APIRouter()

