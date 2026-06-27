from typing import Annotated

from fastapi import Depends, Request

from app.models import User
from core.fastapi.dependencies.authentication import BearerCredentialsDep
from core.fastapi.dependencies.controllers import UserControllerDep


async def get_current_user(
    request: Request,
    user_controller: UserControllerDep,
    _: BearerCredentialsDep,
) -> User:
    """Load the authenticated user for the current request.

    Authentication middleware stores the user identifier on ``request.user``.
    This dependency resolves that identifier to a full user model for endpoint
    handlers.

    :param request: The current FastAPI request.
    :param user_controller: The controller used to load the user.
    :param _: Validated bearer credentials required for dependency ordering.

    :return: The authenticated user model.
    """
    return await user_controller.get_by_id(request.user.id)


CurrentUserDep = Annotated[User, Depends(get_current_user)]
