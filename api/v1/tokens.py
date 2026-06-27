from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.schemas.extras import RefreshTokenRequest, Token
from core.fastapi.dependencies import (
    BearerCredentialsDep,
    UserControllerDep,
)

tokens_router = APIRouter(prefix="/tokens", tags=["Tokens"])


@tokens_router.post("")
async def login(
    user_controller: UserControllerDep,
    credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
) -> Token | None:
    """Credentials are passed as a header in the form of 'Basic username:password'"""
    username = credentials.username
    password = credentials.password

    return await user_controller.login(username, password)


@tokens_router.put("")
async def refresh_token(
    access_token: BearerCredentialsDep,
    token_request: RefreshTokenRequest,
    user_controller: UserControllerDep,
) -> Token | None:
    return await user_controller.refresh_token(
        access_token.credentials, token_request.refresh_token
    )
