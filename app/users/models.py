from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, int_pk, str_uniq


class User(Base):
    id: Mapped[int_pk]

    email: Mapped[str_uniq]
    phone_number: Mapped[str_uniq]

    first_name: Mapped[str]
    last_name: Mapped[str]

    hashed_password: Mapped[str] = mapped_column(nullable=False)

    is_user: Mapped[bool] = mapped_column(
        server_default=text("true"),
        default=True,
        nullable=False,
    )

    is_student: Mapped[bool] = mapped_column(
        server_default=text("false"),
        default=False,
        nullable=False,
    )

    is_teacher: Mapped[bool] = mapped_column(
        server_default=text("false"),
        default=False,
        nullable=False,
    )

    is_admin: Mapped[bool] = mapped_column(
        server_default=text("false"),
        default=False,
        nullable=False,
    )

    is_super_admin: Mapped[bool] = mapped_column(
        server_default=text("false"),
        default=False,
        nullable=False,
    )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"email={self.email!r}, "
            f"first_name={self.first_name!r}, "
            f"last_name={self.last_name!r})"
        )

    def __repr__(self) -> str:
        return str(self)