from fastapi import APIRouter, Depends

from app.controllers import UserController
from app.models import Role
from app.schemas.requests import RegisterUserRequest
from app.schemas.responses import UserResponse
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired, get_current_user
from core.security.require_role import require_role

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post(
    "/me", dependencies=[Depends(AuthenticationRequired)], response_model=UserResponse
)
async def me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@users_router.post(
    "",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(require_role(Role.MODERATOR)),
    ],
    response_model=UserResponse,
)
async def create_user(
    user_request: RegisterUserRequest,
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    return await user_controller.create(user_request.dict())


@users_router.get(
    "",
    dependencies=[Depends(AuthenticationRequired)],
    response_model=list[UserResponse],
)
async def get_users(
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    return await user_controller.get_all()


@users_router.get(
    "/{user_id}",
    dependencies=[Depends(AuthenticationRequired)],
    response_model=UserResponse,
)
async def get_user_by_id(
    user_id: int,
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    return await user_controller.get_by_id(user_id)


@users_router.get(
    "/search/",
    dependencies=[Depends(AuthenticationRequired)],
    response_model=list[UserResponse],
)
async def search_users_by_username(
    query: str, user_controller: UserController = Depends(Factory().get_user_controller)
):
    return await user_controller.search_by_username(query)


@users_router.put(
    "/{user_id}",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(require_role(Role.MODERATOR)),
    ],
    response_model=UserResponse,
)
async def update_user(
    user_id: int,
    user_request: RegisterUserRequest,
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    return await user_controller.update(user_id, user_request.dict())


@users_router.delete(
    "/{user_id}",
    dependencies=[Depends(AuthenticationRequired), Depends(require_role(Role.ADMIN))],
)
async def delete_user(
    user_id: int,
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    return await user_controller.delete(user_id)
