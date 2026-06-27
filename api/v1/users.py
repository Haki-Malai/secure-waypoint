from datetime import datetime

from fastapi import APIRouter, Depends, status

from app.models import Role, User
from app.schemas.requests import (
    RegisterUserRequest,
    UpdateSelfRequest,
    UpdateUserRequest,
    UserPagination,
)
from app.schemas.responses import UserResponse
from core.fastapi.dependencies import (
    AuthenticationRequiredDep,
    CurrentUserDep,
    UserControllerDep,
)
from core.security.require_role import require_role

users_router = APIRouter(tags=["Users"])


@users_router.post(
    "/users",
    dependencies=[
        Depends(require_role(Role.MODERATOR)),
    ],
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_request: RegisterUserRequest,
    user_controller: UserControllerDep,
):
    return await user_controller.create(user_request.to_create_attributes())


@users_router.get(
    "/users",
    dependencies=[AuthenticationRequiredDep],
    response_model=list[UserResponse],
)
async def get_users(
    user_controller: UserControllerDep,
    query_params: UserPagination = Depends(),
):
    filters = []
    if query_params.creation_year:
        start_date = datetime(query_params.creation_year, 1, 1)
        end_date = datetime(query_params.creation_year + 1, 1, 1)
        filters.append(User.created_at.between(start_date, end_date))

    return await user_controller.get_filtered(
        filters=filters, skip=query_params.skip, limit=query_params.limit
    )


@users_router.get(
    "/users/{user_id}",
    dependencies=[AuthenticationRequiredDep],
    response_model=UserResponse,
)
async def get_user_by_id(
    user_id: int,
    user_controller: UserControllerDep,
):
    return await user_controller.get_by_id(user_id)


@users_router.get(
    "/users/search/",
    dependencies=[AuthenticationRequiredDep],
    response_model=list[UserResponse],
)
async def search_users_by_username(query: str, user_controller: UserControllerDep):
    return await user_controller.search_by_username(query)


@users_router.put(
    "/users/{user_id}",
    dependencies=[
        Depends(require_role(Role.MODERATOR)),
    ],
    response_model=UserResponse,
)
async def update_user(
    user_id: int,
    user_request: UpdateUserRequest,
    user_controller: UserControllerDep,
):
    return await user_controller.update(user_id, user_request.to_update_attributes())


@users_router.delete(
    "/users/{user_id}",
    dependencies=[Depends(require_role(Role.ADMIN))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    user_controller: UserControllerDep,
):
    return await user_controller.delete(user_id)


@users_router.get(
    "/me",
    response_model=UserResponse,
)
async def me(current_user: CurrentUserDep):
    return current_user


@users_router.put(
    "/me",
    response_model=UserResponse,
)
async def update_me(
    user_request: UpdateSelfRequest,
    user_controller: UserControllerDep,
    current_user: CurrentUserDep,
):
    return await user_controller.update(
        current_user.id, user_request.to_update_attributes()
    )


@users_router.delete(
    "/me",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_me(
    user_controller: UserControllerDep,
    current_user: CurrentUserDep,
):
    return await user_controller.delete(current_user.id)
