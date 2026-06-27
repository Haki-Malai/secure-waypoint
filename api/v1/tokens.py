from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.controllers import UserController
from app.schemas.extras import RefreshTokenRequest, Token
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired

tokens_router = APIRouter(prefix="/tokens", tags=["Tokens"])


@tokens_router.post("")
async def login(
    credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> Token | None:
    """Credentials are passed as a header in the form of 'Basic username:password'"""
    username = credentials.username
    password = credentials.password

    return await user_controller.login(username, password)


@tokens_router.put("", dependencies=[Depends(AuthenticationRequired)])
async def refresh_token(
    request: Request,
    token_request: RefreshTokenRequest,
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> Token | None:
    access_token = request.headers.get("Authorization").split(" ")[1]
    return await user_controller.refresh_token(
        access_token, token_request.refresh_token
    )
