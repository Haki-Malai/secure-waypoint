from enum import StrEnum

from pydantic import BaseModel, ValidationError

from app.schemas.extras import Token
from core.exceptions import UnauthorizedException
from core.security import jwt_handler


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenPayload(BaseModel):
    user_id: int
    token_type: TokenType


class TokenHelper:
    def issue_pair(self, user_id: int) -> Token:
        return Token(
            access_token=self.encode(user_id=user_id, token_type=TokenType.ACCESS),
            refresh_token=self.encode(user_id=user_id, token_type=TokenType.REFRESH),
        )

    def encode(self, user_id: int, token_type: TokenType) -> str:
        return jwt_handler.encode(
            TokenPayload(user_id=user_id, token_type=token_type).model_dump()
        )

    def decode(
        self,
        token: str,
        expected_type: TokenType | None = None,
    ) -> TokenPayload:
        try:
            payload = TokenPayload.model_validate(jwt_handler.decode(token))
        except ValidationError:
            raise UnauthorizedException("Invalid token")

        if expected_type is not None and payload.token_type != expected_type:
            raise UnauthorizedException("Invalid token")

        return payload

    def validate_refresh(self, access_token: str, refresh_token: str) -> int:
        access_payload = self.decode(access_token, expected_type=TokenType.ACCESS)
        refresh_payload = self.decode(refresh_token, expected_type=TokenType.REFRESH)

        if access_payload.user_id != refresh_payload.user_id:
            raise UnauthorizedException("Invalid token")

        return access_payload.user_id


token_helper = TokenHelper()
