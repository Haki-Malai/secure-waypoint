from typing import Annotated

from fastapi import Depends

from app.controllers import UserController
from core.factory import Factory

factory = Factory()

UserControllerDep = Annotated[UserController, Depends(factory.get_user_controller)]
