import sqlalchemy as sa
import sqlalchemy.orm as so

from core.database import Base
from core.database.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String)

    def __repr__(self) -> str:
        return f"<User {self.username}>"
