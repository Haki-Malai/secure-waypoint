from sqlalchemy.future import select

from app.models.user import User
from core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    async def search_by_username(self, query: str) -> list[User]:
        """Search for users by username using a query.

        :param query: The query to search for.

        :return: A list of users that match the query.
        """
        async with self.session() as session:
            result = await session.execute(
                select(User).filter(User.username.ilike(f"%{query}%"))
            )
            return result.scalars().all()
