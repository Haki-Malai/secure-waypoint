from app.models import Role
from core.exceptions import ForbiddenException
from core.fastapi.dependencies import CurrentUserDep


def require_role(required_role: Role):
    """Create a dependency that enforces a minimum user role.

    :param required_role: The lowest role allowed to access the endpoint.

    :return: A FastAPI dependency that returns the current user when permitted.
    """

    def role_checker(current_user: CurrentUserDep):
        if current_user.role.value < required_role.value:
            raise ForbiddenException("Insufficient permissions")
        return current_user

    return role_checker
