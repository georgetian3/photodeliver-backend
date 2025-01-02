from uuid import UUID
from fastapi import APIRouter


user_router = APIRouter()

@user_router.get("/users/{user_id}")
async def get_user(user_id: UUID):
    ...

@user_router.put("/users")
async def create_user():
    ...

@user_router.post("/users/{user_id}")
async def modify_user(user_id: UUID):
    ...

@user_router.delete("/users/{user_id}")
async def delete_user(user_id: UUID):
    ...