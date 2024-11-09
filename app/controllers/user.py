from app.models import User
from app.repositories import UserRepository
from core.controller import BaseController


class UserController(BaseController[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    async def search_by_username(self, query: str) -> list[User]:
        """Search for users by username using a query.

        :param query: The query to search for.

        :return: A list of users that match the query.
        """
        return await self.user_repository.search_by_username(query)
