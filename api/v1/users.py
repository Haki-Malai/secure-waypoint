from fastapi import APIRouter, Depends

from app.controllers import UserController
from app.schemas.requests import RegisterUserRequest
from app.schemas.responses import UserResponse
from core.factory import Factory

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("", response_model=UserResponse)
async def create_user(
    user_request: RegisterUserRequest,
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    return await user_controller.create(user_request.dict())


@users_router.get("", response_model=list[UserResponse])
async def get_users(
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    return await user_controller.get_all()


@users_router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    return await user_controller.get_by_id(user_id)


@users_router.get("/search/", response_model=list[UserResponse])
async def search_users_by_username(
    query: str, user_controller: UserController = Depends(Factory().get_user_controller)
):
    return await user_controller.search_by_username(query)


@users_router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_request: RegisterUserRequest,
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    return await user_controller.update(user_id, user_request.dict())
