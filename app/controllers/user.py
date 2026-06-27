from collections.abc import Sequence

from app.helpers import token_helper
from app.models import User
from app.repositories import UserRepository
from app.schemas.extras import Token
from core.controller import BaseController
from core.exceptions import NotFoundException, UnauthorizedException


class UserController(BaseController[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    async def search_by_username(self, query: str) -> Sequence[User]:
        """Search for users by username using a query.

        :param query: The query to search for.

        :return: A list of users that match the query.
        """
        return await self.user_repository.search_by_username(query)

    async def login(self, username: str, password: str) -> Token | None:
        """Login a user with a username and password.

        :param username: The username of the user.
        :param password: The password of the user.

        :return: True if the login is successful, False otherwise.
        """
        user = await self.user_repository.get_by_username(username)
        if user and user.verify_password(password):
            return token_helper.issue_pair(user.id)
        raise UnauthorizedException("Invalid username or password")

    async def refresh_token(
        self, access_token: str, refresh_token: str
    ) -> Token | None:
        """Refresh a token.

        :param token: The token to refresh.

        :return: A new token.
        """
        try:
            user_id = token_helper.validate_refresh(access_token, refresh_token)
            await self.get_by_id(user_id)
            return token_helper.issue_pair(user_id)
        except (KeyError, NotFoundException):
            raise UnauthorizedException("Invalid token")
