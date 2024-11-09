from fastapi import APIRouter, Depends

from app.controllers import UserController
from app.schemas.responses import UserResponse
from core.factory import Factory

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("", response_model=list[UserResponse])
async def get_users(
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    users = await user_controller.get_all()
    return users


@users_router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    user = await user_controller.get_by_id(user_id)
    return user


@users_router.get("/search/", response_model=list[UserResponse])
async def search_users_by_username(
    query: str, user_controller: UserController = Depends(Factory().get_user_controller)
):
    users = await user_controller.search_by_username(query)
    return users
