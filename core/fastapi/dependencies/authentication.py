from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.exceptions.base import UnauthorizedException

OptionalBearerCredentialsDep = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(HTTPBearer(auto_error=False)),
]


async def require_authentication(
    request: Request,
    access_token: OptionalBearerCredentialsDep,
) -> HTTPAuthorizationCredentials:
    """Require a valid authenticated request.

    The authentication middleware populates ``request.auth`` and
    ``request.user``. This dependency verifies that a bearer token was provided
    and that the middleware accepted it before returning the token credentials
    to downstream handlers.

    :param request: The current FastAPI request.
    :param access_token: Optional bearer credentials extracted from the header.

    :raises UnauthorizedException: If no token is provided or authentication
        failed.

    :return: The validated bearer credentials.
    """
    if not access_token:
        raise UnauthorizedException("Access token is required")
    if "authenticated" not in request.auth.scopes:
        raise UnauthorizedException("Invalid access token")

    return access_token


AuthenticationRequired = require_authentication
AuthenticationRequiredDep = Depends(require_authentication)
BearerCredentialsDep = Annotated[
    HTTPAuthorizationCredentials,
    Depends(require_authentication),
]
