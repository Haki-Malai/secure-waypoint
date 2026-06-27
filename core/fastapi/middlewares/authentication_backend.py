from starlette.authentication import (
    AuthCredentials,
)
from starlette.authentication import (
    AuthenticationBackend as BaseAuthenticationBackend,
)
from starlette.requests import HTTPConnection

from app.helpers import TokenType, token_helper
from app.schemas.extras import CurrentUser
from core.exceptions import UnauthorizedException


class AuthenticationBackend(BaseAuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, CurrentUser] | None:
        """Authenticates the user based on the Authorization header.

        :param conn: The HTTP connection.

        :returns: The authentication credentials and the current user.
        """
        authorization: str = conn.headers.get("Authorization", "")
        scheme, token = self._extract_token(authorization)

        if scheme != "bearer" or not token:
            return None

        try:
            payload = token_helper.decode(token, expected_type=TokenType.ACCESS)
        except UnauthorizedException:
            return None

        current_user = CurrentUser(id=payload.user_id)
        return AuthCredentials(["authenticated"]), current_user

    def _extract_token(self, authorization: str) -> tuple[str, str | None]:
        """Extracts the token type and token value from the authorization header.

        :param authorization: The authorization header.

        :returns: The token type and token value.
        """
        try:
            scheme, token = authorization.strip().split(" ", 1)
            return scheme.lower(), token
        except ValueError:
            return "", None
