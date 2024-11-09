from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.controllers import UserController
from app.schemas.extras import Token
from core.factory import Factory

tokens_router = APIRouter(prefix="/tokens", tags=["Tokens"])


@tokens_router.post("")
async def login(
    credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> Token:
    """Credentials are passed as a header in the form of 'Basic username:password'"""
    username = credentials.username
    password = credentials.password

    return await user_controller.login(username, password)
