from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from core.database import Base
from core.exceptions import BadRequestException, NotFoundException
from core.repository import BaseRepository

ModelType = TypeVar("ModelType", bound=Base)


class BaseController(Generic[ModelType]):
    """Base class for data controllers."""

    def __init__(self, model: type[ModelType], repository: BaseRepository):
        self.model_class = model
        self.repository = repository

    async def get_by_user_id(self, user_id: int) -> ModelType:
        try:
            result = await self.repository.get_by(
                field="user_id", value=user_id, unique=True
            )
            if result:
                return result
            else:
                raise NotFoundException(
                    f"EventMapping with user_id: {user_id} does not exist"
                )
        except Exception as e:
            raise e

    async def get_by_id(self, id_: int) -> ModelType:
        """Returns the model instance matching the id.

        :param id_: The id to match.

        :return: The model instance.
        """

        db_obj = await self.repository.get_by(field="id", value=id_, unique=True)
        if not db_obj:
            raise NotFoundException(
                f"{self.model_class.__tablename__.title()} with id: {id} does not exist"
            )

        return db_obj

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """Returns a list of records based on pagination params.

        :param skip: The number of records to skip.
        :param limit: The number of records to return.

        :return: A list of records.
        """

        return await self.repository.get_all(skip, limit)

    async def create(self, attributes: dict[str, Any]) -> ModelType:
        """Creates a new Object in the DB.

        :param attributes: The attributes to create the object with.

        :return: The created object.
        """
        try:
            return await self.repository.create(attributes)
        except IntegrityError as e:
            raise BadRequestException(f"Database Integrity Error: {e.orig}")

    async def update(self, id_: int, attributes: dict[str, Any]) -> ModelType:
        """Updates the Object in the DB.

        :param id_: The id of the object to update.
        :param attributes: The attributes to update the object with.

        :return: The updated object.
        """
        db_obj = await self.get_by_id(id_)
        return await self.repository.update(db_obj, attributes)

    async def delete(self, id_: int) -> None:
        """Deletes the Object from the DB.

        :param id_: The id of the object to delete.

        :return: True if the object was deleted, False otherwise.
        """
        db_obj = await self.get_by_id(id_)
        return await self.repository.delete(db_obj)

    @staticmethod
    async def extract_attributes_from_schema(
        schema: BaseModel, excludes: set = None
    ) -> dict[str, Any]:
        """Extracts the attributes from the schema.

        :param schema: The schema to extract the attributes from.
        :param excludes: The attributes to exclude.

        :return: The attributes.
        """

        return await schema.dict(exclude=excludes, exclude_unset=True)
