from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from core.config import config
from core.exceptions import UnauthorizedException


class JWTHandler:
    secret_key = config.SECRET_KEY
    algorithm = config.JWT_ALGORITHM
    expire_minutes = config.JWT_EXPIRE_MINUTES

    def encode(self, payload: Mapping[str, Any]) -> str:
        """Encode claims into a signed JWT.

        The configured expiration interval is added to a copy of the supplied
        payload so callers do not have their mapping mutated.

        :param payload: Claims to include in the token.

        :return: The encoded JWT string.
        """
        expire = datetime.now(UTC) + timedelta(minutes=self.expire_minutes)
        claims = dict(payload)
        claims.update({"exp": expire})
        return jwt.encode(claims, self.secret_key, algorithm=self.algorithm)

    def decode(self, token: str) -> dict[str, Any]:
        """Decode and validate a signed JWT.

        :param token: The JWT string to decode.

        :raises UnauthorizedException: If the token is malformed, expired, or
            fails signature validation.

        :return: The decoded token claims.
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            raise UnauthorizedException("Invalid token")


jwt_handler: JWTHandler = JWTHandler()
