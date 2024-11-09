from typing import Any, Generic, TypeVar
from uuid import UUID

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

    async def get_by_user_id(
        self, user_id: int, join_: set[str] | None = None
    ) -> ModelType:
        try:
            result = await self.repository.get_by(
                field="user_id", value=user_id, join_=join_, unique=True
            )
            if result:
                return result
            else:
                raise NotFoundException(
                    f"EventMapping with user_id: {user_id} does not exist"
                )
        except Exception as e:
            raise e

    async def get_by_id(self, id_: int, join_: set[str] | None = None) -> ModelType:
        """Returns the model instance matching the id.

        :param id_: The id to match.
        :param join_: The joins to make.

        :return: The model instance.
        """

        db_obj = await self.repository.get_by(
            field="id", value=id_, join_=join_, unique=True
        )
        if not db_obj:
            raise NotFoundException(
                f"{self.model_class.__tablename__.title()} with id: {id} does not exist"
            )

        return db_obj

    async def get_by_uuid(self, uuid: UUID, join_: set[str] | None = None) -> ModelType:
        """Returns the model instance matching the uuid.

        :param uuid: The uuid to match.
        :param join_: The joins to make.

        :return: The model instance.
        """

        db_obj = await self.repository.get_by(
            field="uuid", value=uuid, join_=join_, unique=True
        )
        if not db_obj:
            raise NotFoundException(
                f"{self.model_class.__tablename__.title()} with id: {uuid} does not exist"
            )
        return db_obj

    async def get_all(
        self, skip: int = 0, limit: int = 100, join_: set[str] | None = None
    ) -> list[ModelType]:
        """Returns a list of records based on pagination params.

        :param skip: The number of records to skip.
        :param limit: The number of records to return.
        :param join_: The joins to make.

        :return: A list of records.
        """

        response = await self.repository.get_all(skip, limit, join_)
        return response

    async def create(self, attributes: dict[str, Any]) -> ModelType:
        """Creates a new Object in the DB.

        :param attributes: The attributes to create the object with.

        :return: The created object.
        """
        try:
            return await self.repository.create(attributes)
        except IntegrityError as e:
            raise BadRequestException(f"Database Integrity Error: {e.orig}")

    async def delete(self, model: ModelType) -> bool:
        """Deletes the Object from the DB.

        :param model: The model to delete.

        :return: True if the object was deleted, False otherwise.
        """
        delete = await self.repository.delete(model)
        return delete

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
