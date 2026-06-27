from functools import partial
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import UserController
from app.models import User
from app.repositories import UserRepository
from core.database import get_session

DatabaseSessionDep = Annotated[AsyncSession, Depends(get_session)]


class Factory:
    user_repository = partial(UserRepository, User)

    def get_user_controller(self, db_session: DatabaseSessionDep) -> UserController:
        """Create a user controller bound to the current database session.

        :param db_session: The FastAPI-injected async database session.

        :return: A user controller configured with a user repository.
        """
        return UserController(
            user_repository=self.user_repository(db_session=db_session)
        )
